if command -v pnpm >/dev/null 2>&1; then
  cd client
  pnpm install
  pnpm run build
  cd ..
else
  echo "Warning: pnpm is not installed. You should compile the client manually."
fi

if [ -d "./release" ]; then
  echo "Removing old release directory"
  rm -r "./release"
fi
mkdir -p "./release"

cp main.py "./release"
cp ./requirements.txt "./release"
cp ./README.md "./release"
cp .gitingore "./release"
cp LICENSE "./release"
cp ./kernel ./release
cp ./static ./release
cp ./data/config.yml ./release/data
cp ./data/sentiment ./release/data
cp ./data/models/facial.pth ./release/data/models
cp ./client/dist ./release/client

cp ./build.sh "./release"

echo "Build complete. You can now run the server by executing 'uvicorn main:app --reload' in the release directory."
