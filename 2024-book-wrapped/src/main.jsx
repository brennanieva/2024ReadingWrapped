import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { WrappedProvider } from './context/WrappedContext'  // ✅ add this

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <WrappedProvider>               {/* ✅ wrap the app here */}
      <App />
    </WrappedProvider>
  </StrictMode>,
)