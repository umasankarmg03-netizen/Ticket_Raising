from google.generativeai import GenerativeModel, configure

configure(api_key="AIzaSyDOHKDzvv1BbAD-9CxWN4Tu5tnQysNXcKk")

gem = GenerativeModel("gemini-2.5-flash")

try:
    response = gem.generate_content("Hello world")
    print(response.text)
except Exception as e:
    print("Error:", e)
