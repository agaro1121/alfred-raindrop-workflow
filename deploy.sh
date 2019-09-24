if [ ! -d lib ]; then
    echo "Creating lib directory..."
    mkdir lib
fi

echo "Fetching 3rd party libs..."
pip install --target=lib requests > /dev/null 2>&1
pip install --target=lib futures > /dev/null 2>&1

if [ -f raindrop.alfredworkflow ]; then
    rm raindrop.alfredworkflow
fi    

echo "Creating alfred workflow..."
zip raindrop.alfredworkflow icon.png info.plist -r lib -r raindrop > /dev/null 2>&1
echo "Complete!"