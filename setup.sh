OS="$(uname -s)"

if [ "$OS" = "Linux" ]; then
  if ! command -v apt >/dev/null 2>&1; then
    echo "Warning: APT is not installed. You should manually install PortAudio."
  fi
  sudo apt update
  sudo apt install portaudio19-dev
elif [ "$OS" = "Darwin" ]; then
  if ! command -v brew >/dev/null 2>&1; then
    echo "Homebrew is not installed. Please install Homebrew and try again."
    exit 1
  fi
  brew install portaudio
fi

pip install -r requirements.txt
pip install uvicorn
pip install 'httpx[socks]'
python -m spacy download en_core_web_sm

if curl --head --silent --fail https://aurora-echo.zzdev.org > /dev/null; then
  echo "URL is accessible. You can open the client by visiting https://aurora-echo.zzdev.org."
else
  echo "URL is not accessible. Please use python -m http.server -d ./data/client to serve the client."
fi

echo "Setup complete. You can now run the server by executing 'uvicorn main:app --reload' in the release directory."
