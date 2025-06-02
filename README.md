1. Start Kafka + Zookeeper using Docker

```bash
# Stop all running containers (if needed)
docker stop $(docker ps -aq)

# Start Zookeeper and Kafka
docker-compose up -d

2. Install Python dependencies
pip install -r requirements.txt

3. Train the ML model
cd ml_model
python train_model.py

4. Start the consumer for predictions
cd consumer
python sunlight_prediction.py

5. Start the Kafka producers in separate terminals
Terminal 1: Cafe Producer
cd kafka
python cafe_producer.py

Terminal 2: Weather Producer
cd kafka
python weather_producer.py

6. Launch Streamlit dashboard
cd dashboard
streamlit run app.py
