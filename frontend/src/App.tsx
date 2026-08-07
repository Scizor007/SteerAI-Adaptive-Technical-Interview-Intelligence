import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { LandingPage } from './features/landing';
import { CandidateSelectionPage } from './features/candidates';
import { InterviewWorkspacePage } from './features/interview';
import { FeedbackPage } from './features/feedback';
import { ArchitecturePage } from './features/architecture';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/candidates" element={<CandidateSelectionPage />} />
        <Route path="/interview/:candidateId" element={<InterviewWorkspacePage />} />
        <Route path="/feedback/:candidateId" element={<FeedbackPage />} />
        <Route path="/architecture" element={<ArchitecturePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
