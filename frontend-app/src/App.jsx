import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import AuthProvider from "./contexts/AuthProvider"
import PrivateRoute from "./routes/PrivateRoute"
import PublicRoute from "./routes/PublicRoute"

import Login from "./pages/Login"
import Register from "./pages/Register"
import Dashboard from "./pages/Dashboard"
import Conversation from "./pages/Conversation"
import Company from "./pages/Company"
import Home from "./pages/Home";
import ConversationDetail from "./pages/ConversationDetail";

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="h-full bg-white">
          <Routes>
            <Route path="/" element={<PublicRoute><Home /></PublicRoute>} />

            <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
            <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />

            <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
            
            <Route path="/dashboard/:companySlug" element={<PrivateRoute><Company /></PrivateRoute>} />

            <Route path="/conversations" element={<PrivateRoute><Conversation /></PrivateRoute>} />
            <Route path="/conversations/:companySlug" element={<PrivateRoute><ConversationDetail /></PrivateRoute>} />

            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App
