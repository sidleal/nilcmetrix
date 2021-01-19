docker run --name pgs_cohmetrix -v $PWD:/shared -e POSTGRES_USER=cohmetrix -e POSTGRES_PASSWORD=cohmetrix -d --restart always postgres
