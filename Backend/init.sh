echo "🚀 Initializing Spotify Music Recommender Project..."

pkg update -y && pkg upgrade -y
pkg install python git -y

echo "📦 Creating virtual environment..."
python -m venv venv

source venv/bin/activate

echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📁 Creating project folders..."
mkdir -p spotify recommender datasets models
touch spotify/__init__.py recommender/__init__.py

echo "✅ Setup complete!"
echo "To start your FastAPI app:"
echo "source venv/bin/activate && uvicorn main:app --reload"
