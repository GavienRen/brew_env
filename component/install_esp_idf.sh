# install esp-idf
mkdir -p ~/esp && cd ~/esp && git clone --recursive https://github.com/espressif/esp-idf.git &&
    cd ~/esp/esp-idf && ./install.sh all && echo "source ~/esp/esp-idf/export.sh" >>~/.zshrc

# Run the following command to source the environment variables
# source ~/esp/esp-idf/export.sh
# idf.py --version

# Create a new example project
# cp -r $IDF_PATH/examples/get-started/hello_world .
# cd hello_world
# idf.py set-target esp32-s3
# idf.py build
