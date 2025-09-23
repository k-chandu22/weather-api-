import requests
import json
import gradio as gr

def get_weather_data(api_key, city="hyderabad"):

    url = "http://api.weatherapi.com/v1/current.json"
    
    params = {
        "key": api_key,
        "q": city
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        weather_data = response.json()
        return weather_data
        
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return None

def display_weather(weather_data):
   
    if not weather_data:
        print("No weather data available")
        return
    
    try:
        location = weather_data.get('location', {})
        current = weather_data.get('current', {})
        
        print("=" * 50)
        print("CURRENT WEATHER REPORT")
        print("=" * 50)
        print(f"Location: {location.get('name', 'N/A')}, {location.get('region', 'N/A')}, {location.get('country', 'N/A')}")
        print(f"Local Time: {location.get('localtime', 'N/A')}")
        print(f"Temperature: {current.get('temp_c', 'N/A')}°C ({current.get('temp_f', 'N/A')}°F)")
        print(f"Condition: {current.get('condition', {}).get('text', 'N/A')}")
        print(f"Humidity: {current.get('humidity', 'N/A')}%")
        print(f"Wind Speed: {current.get('wind_kph', 'N/A')} km/h")
        print(f"Pressure: {current.get('pressure_mb', 'N/A')} mb")
        print(f"UV Index: {current.get('uv', 'N/A')}")
        print("=" * 50)
        
    except Exception as e:
        print(f"Error displaying weather data: {e}")

def gradio_weather_function(city):
    
    if not city.strip():
        return "Please enter a city name."
    
    # Use the API key directly from the script
    API_KEY = api_key
    
    weather_data = get_weather_data(API_KEY, city)
    
    if not weather_data:
        return "Error: Could not fetch weather data. Please check your city name."
    
    # Format weather data for display
    try:
        location = weather_data.get('location', {})
        current = weather_data.get('current', {})
        
        formatted_text = f"""
🌤️ **CURRENT WEATHER REPORT** 🌤️

📍 **Location:** {location.get('name', 'N/A')}, {location.get('region', 'N/A')}, {location.get('country', 'N/A')}
🕐 **Local Time:** {location.get('localtime', 'N/A')}

🌡️ **Temperature:** {current.get('temp_c', 'N/A')}°C ({current.get('temp_f', 'N/A')}°F)
☁️ **Condition:** {current.get('condition', {}).get('text', 'N/A')}
💧 **Humidity:** {current.get('humidity', 'N/A')}%
💨 **Wind Speed:** {current.get('wind_kph', 'N/A')} km/h
📊 **Pressure:** {current.get('pressure_mb', 'N/A')} mb
☀️ **UV Index:** {current.get('uv', 'N/A')}
        """
        
        return formatted_text
        
    except Exception as e:
        return f"Error displaying weather data: {e}"

def create_gradio_interface():
   
    with gr.Blocks(title="Weather API Dashboard", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🌤️ Weather API Dashboard")
        gr.Markdown("Enter a city name to get current weather information.")
        
        with gr.Row():
            with gr.Column(scale=1):
                city_input = gr.Textbox(
                    label="City Name",
                    placeholder="Enter city name (e.g., hyderabad, london, new york)",
                    value="hyderabad"
                )
                
                submit_btn = gr.Button("Get Weather", variant="primary", size="lg")
                
            with gr.Column(scale=2):
                weather_output = gr.Markdown(
                    label="Weather Information",
                    value="Enter a city name to get weather data..."
                )
        
        
        # Event handlers
        submit_btn.click(
            fn=gradio_weather_function,
            inputs=[city_input],
            outputs=[weather_output]
        )
        
        # Allow Enter key to submit
        city_input.submit(
            fn=gradio_weather_function,
            inputs=[city_input],
            outputs=[weather_output]
        )
    
    return interface

if __name__ == "__main__":
    # Create and launch Gradio interface
    interface = create_gradio_interface()
    interface.launch(
        share=False,  # Set to True if you want a public link
        server_name="127.0.0.1",  # Local host
        server_port=7860,  # Default Gradio port
        show_error=True
    )

