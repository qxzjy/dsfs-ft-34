import requests
payload = {
  "title": "This is my great blog title",
   "content": "This is the body of my article",
   "Author": "Jaskier"
}
r = requests.post("http://localhost:7860/predict", json={
  "YearsExperience": 0
})
print(r.content)