body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: #0f172a;
  color: white;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 24px;
}

.header {
  margin-bottom: 30px;
}

.header h1 {
  margin-bottom: 8px;
}

.panel {
  background: #111827;
  padding: 22px;
  border-radius: 14px;
  margin-bottom: 20px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}

form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

label {
  font-weight: 600;
}

input {
  padding: 12px 14px;
  border-radius: 10px;
  border: 1px solid #374151;
  background: #0f172a;
  color: white;
}

button {
  border: none;
  background: linear-gradient(135deg, #f97316, #fb7185);
  color: white;
  border-radius: 10px;
  padding: 12px 16px;
  font-weight: 700;
  cursor: pointer;
}

.checkbox-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.time-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.result-panel {
  min-height: 200px;
}
