(function(){
    var stage, textStage;
    var circles, textPixels, textFormed;
    var offsetX, offsetY, text;
    var colors = ['#a1bdff', '#365fa9', '#7391b0', '#627dac', '#7876a7'];

    function init() {
        initStages();
        initCircles();
        animate();
        // $('#text').focus();
    }

    // Init Canvas
    function initStages() {
        stage = new createjs.Stage("stage");
        stage.canvas.width = window.innerWidth*2;
        stage.canvas.height = 200;//window.innerHeight;

        var shape = new createjs.Shape();
        shape.graphics.beginLinearGradientFill(["#334191","#4764a0","#718fc8"], [0, .7, 1], 0, 80, 0, 200).drawRect(0, 0, window.innerWidth * 2, 200);
          
        stage.addChild(shape);
    }


    function initCircles() {
        circles = [];
        for(var i=0; i<100; i++) {
            var circle = new createjs.Shape();
            var r = 60;
            var x = window.innerWidth*Math.random();
            var y = window.innerHeight*Math.random();
            var color = colors[Math.floor(i%colors.length)];
            var alpha = 0.05 + Math.random()*0.3;
            circle.alpha = alpha;
            circle.radius = r;
            circle.graphics.beginFill(color).drawCircle(0, 0, r);
            circle.x = x;
            circle.y = y;
            circles.push(circle);
            stage.addChild(circle);
            circle.movement = 'float';
            tweenCircle(circle);
        }
    }


    // animating circles
    function animate() {
        stage.update();
        requestAnimationFrame(animate);
    }

    function tweenCircle(c, dir) {
        if(c.tween) c.tween.kill();
        if(dir == 'in') {
            c.tween = TweenLite.to(c, 0.4, {x: c.originX, y: c.originY, ease:Quad.easeInOut, alpha: 1, radius: 5, scaleX: 0.4, scaleY: 0.4, onComplete: function() {
                c.movement = 'jiggle';
                tweenCircle(c);
            }});
        } else if(dir == 'out') {
            c.tween = TweenLite.to(c, 0.8, {x: window.innerWidth*Math.random(), y: window.innerHeight*Math.random(), ease:Quad.easeInOut, alpha: 0.1 + Math.random()*0.5, scaleX: 1, scaleY: 1, onComplete: function() {
                c.movement = 'float';
                tweenCircle(c);
            }});
        } else {
            if(c.movement == 'float') {
                c.tween = TweenLite.to(c, 5 + Math.random()*3.5, {x: c.x + -100+Math.random()*200, y: c.y + -100+Math.random()*200, ease:Quad.easeInOut, alpha: 0.1 + Math.random()*0.5,
                    onComplete: function() {
                        tweenCircle(c);
                    }});
            } else {
                c.tween = TweenLite.to(c, 0.05, {x: c.originX + Math.random()*3, y: c.originY + Math.random()*3, ease:Quad.easeInOut,
                    onComplete: function() {
                        tweenCircle(c);
                    }});
            }
        }
    }


    window.onload = function() { init() };
})();

