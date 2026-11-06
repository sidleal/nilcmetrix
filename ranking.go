package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/gorilla/websocket"
	"github.com/sidleal/simpligo-cloze/web/tools/senter"
)

var simpligoRankingURI = "http://simpligo-ranking:8080/api/v1/ranking/ranking3f"

type SimpligoRankingResultItem struct {
	Index    int    `json:"i"`
	Sentence string `json:"s"`
	Value    int    `json:"v"`
	Color    string `json:"c"`
}

type WSRankingResponse struct {
	Status  string                      `json:"status"` // "processing", "success", "error"
	Message string                      `json:"message"`
	Results []SimpligoRankingResultItem `json:"results,omitempty"`
}

func simpligoRankingHandler(w http.ResponseWriter, r *http.Request) {
	pInfo := pageInfo
	pInfo.ShowResults = false
	// Just serve the template. JS will handle the rest.
	templateHandler(w, r, "ranking", pInfo)
}

func wsRankingHandler(w http.ResponseWriter, r *http.Request) {
	// Upgrade the HTTP connection to a WebSocket connection
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("WebSocket Upgrade error:", err)
		return
	}
	defer conn.Close()

	// 1. Read the incoming request
	var req WSRequest
	err = conn.ReadJSON(&req)
	if err != nil {
		conn.WriteJSON(WSRankingResponse{Status: "error", Message: "Invalid request formatting."})
		return
	}

	// 2. Validations
	nWords := strings.Count(req.Text, " ") + 1
	if nWords > 1000 {
		conn.WriteJSON(WSRankingResponse{Status: "error", Message: "Text is too big. / Texto muito longo."})
		return
	}

	remoteIP := strings.Split(r.RemoteAddr, ":")[0]
	isHuman := ValidateTurnstile(req.Captcha, remoteIP)
	if !isHuman {
		conn.WriteJSON(WSRankingResponse{Status: "error", Message: "Invalid Re-Captcha Validation."})
		return
	}

	// 3. Notify the frontend that processing has started
	conn.WriteJSON(WSRankingResponse{Status: "processing", Message: "Analisando o texto, por favor aguarde... (Processing, wait...)"})

	// Keep alive
	// Create a channel to signal when the processing is done
	done := make(chan bool)

	// Start a Goroutine to send a Ping every 15 seconds
	go func() {
		ticker := time.NewTicker(15 * time.Second)
		defer ticker.Stop()

		for {
			select {
			case <-ticker.C:
				// WriteControl is safe to call concurrently with WriteJSON in gorilla/websocket
				if err := conn.WriteControl(websocket.PingMessage, []byte{}, time.Now().Add(time.Second)); err != nil {
					log.Println("Ping error or connection closed:", err)
					return
				}
			case <-done:
				// The process finished, stop sending pings
				return
			}
		}
	}()

	// 4. Run ranking calculation
	env_URI := os.Getenv("SIMPLIGO_RANKING_URI")
	if len(strings.TrimSpace(env_URI)) > 0 {
		simpligoRankingURI = env_URI
	}
	log.Println(simpligoRankingURI)

	jsonFeatsList := "["
	sentList := []string{}
	parsed := senter.ParseText(req.Text)
	for _, p := range parsed.Paragraphs {
		for _, s := range p.Sentences {
			_, list, err := callMetrix("_all", s.Text)
			if err != nil {
				log.Println(err)
				conn.WriteJSON(WSRankingResponse{Status: "error", Message: "Error processando texto: " + err.Error()})
				return
			}
			jsonFeatsList += metrixResultToJSON(list) + ","
			sentList = append(sentList, s.Text)
		}
	}
	jsonFeatsList = strings.Trim(jsonFeatsList, ",") + "]"

	list := callSimpligoRanking(jsonFeatsList)
	var rankingList []SimpligoRankingResultItem
	for i, v := range list {
		if i >= len(sentList) {
			break
		}
		it := SimpligoRankingResultItem{}
		it.Index = i + 1
		it.Sentence = sentList[i]
		floatValue, _ := strconv.ParseFloat(v, 64)
		it.Value = int(floatValue * 100)

		if it.Value < 26 {
			it.Color = "green"
		} else if it.Value < 51 {
			it.Color = "orange"
		} else if it.Value < 76 {
			it.Color = "darkorange"
		} else {
			it.Color = "red"
		}

		rankingList = append(rankingList, it)
	}

	conn.WriteJSON(WSRankingResponse{Status: "success", Results: rankingList})
}

func simpligoRankingHandlerOld(w http.ResponseWriter, r *http.Request) {

	env_URI := os.Getenv("SIMPLIGO_RANKING_URI")
	if len(strings.TrimSpace(env_URI)) == 0 {
		simpligoRankingURI = env_URI
	}
	log.Println(simpligoRankingURI)

	pInfo := pageInfo
	pInfo.ShowResults = false

	text := r.FormValue("text")

	if text != "" {

		nWords := strings.Count(text, " ") + 1
		if nWords > 1000 {
			ret := "Text is too big. / Texto muito longo."
			log.Println(ret)
			pInfo.Message = ret
			pInfo.ShowMessage = true

		} else {

			jsonFeatsList := "["
			sentList := []string{}
			parsed := senter.ParseText(text)
			for _, p := range parsed.Paragraphs {
				for _, s := range p.Sentences {
					_, list, err := callMetrix("_all", s.Text)
					if err != nil {
						log.Println(err)
						w.WriteHeader(http.StatusInternalServerError)
						fmt.Fprint(w, "Error "+err.Error())
						return
					}
					jsonFeatsList += metrixResultToJSON(list) + ","
					sentList = append(sentList, s.Text)
				}
			}
			jsonFeatsList = strings.Trim(jsonFeatsList, ",") + "]"

			list := callSimpligoRanking(jsonFeatsList)
			for i, v := range list {
				it := SimpligoRankingResultItem{}
				it.Index = i + 1
				it.Sentence = sentList[i]
				floatValue, _ := strconv.ParseFloat(v, 64)
				it.Value = int(floatValue * 100)

				if it.Value < 26 {
					it.Color = "green"
				} else if it.Value < 51 {
					it.Color = "orange"
				} else if it.Value < 76 {
					it.Color = "darkorange"
				} else {
					it.Color = "red"
				}

				pInfo.SimpligoRankingList = append(pInfo.SimpligoRankingList, it)
			}

			pInfo.ShowResults = true
			pInfo.Text = text
		}
	}

	templateHandler(w, r, "ranking", pInfo)
}

func callSimpligoRanking(featList string) []string {
	ret := []string{}

	resp, err := http.Post(simpligoRankingURI, "text", bytes.NewReader([]byte(featList)))
	if err != nil {
		log.Println("Error: " + err.Error())
		return ret
	}

	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Println("Error reading response: " + err.Error())
		return ret
	}

	log.Println(string(body))
	ret = strings.Split(string(body), ",")

	return ret
}
