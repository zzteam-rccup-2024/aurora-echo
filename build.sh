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
cp -r ./kernel ./release
cp -r ./static ./release
cp -r ./data/config.yml ./release/data
cp -r ./data/sentiment ./release/data
cp ./data/models/facial.pth ./release/data/models
cp -r ./client/dist ./release/client
cp ./setup.sh "./release"

cp ./build.sh "./release"
cp ./build.ps1 "./release"

echo "Build complete. You can now run the server by executing 'uvicorn main:app --reload' in the release directory."
