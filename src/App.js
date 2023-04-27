import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Profile from './components/Profile';
import Films from './components/Films';
import Schedule from './components/Schedule';

function App() {
  return (
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Profile />} />
          <Route path="/films" element={<Films />} />
          <Route path="/schedule" element={<Schedule />} />
        </Routes>
      </Router>
  );
}

export default App;
