run:
	docker build -t rutigs/gaming_blog --file docker/Dockerfile .
	docker run --publish 8000:8000 rutigs/gaming_blog:latest

test:
	# Testing for Django Backend
	docker build -t rutigs/gaming_blog_test --file docker/testDockerfile .
	docker run -t rutigs/gaming_blog_test
