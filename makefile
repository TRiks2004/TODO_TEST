

# tools
# ------------------------------------------------------------------------------------

addHeader:
	python ./tools/create_headers_env.py "$(HEADER)"

# ------------------------------------------------------------------------------------

# docker
# ------------------------------------------------------------------------------------

build-setup:
	sudo docker compose -f dokcercompose.yaml up -d --build

# ------------------------------------------------------------------------------------

# formatter
# ------------------------------------------------------------------------------------

formatter-black:
	black --config formatter_config/.black .

formatter: formatter-black

# ------------------------------------------------------------------------------------
