import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchInteractions, toggleView } from './store/interactionSlice';
import LogInteractionForm from './components/LogInteractionForm';
import ChatInterface from './components/ChatInterface';
import InteractionList from './components/InteractionList';

function App() {
  const dispatch = useDispatch();
  const { showForm, showChat, interactions } = useSelector(state => state.interactions);

  useEffect(() => {
    dispatch(fetchInteractions());
  }, [dispatch]);

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>AI-First CRM - HCP Module</h1>
        <p>Log and manage Healthcare Professional interactions</p>
      </header>

      <main className="app-main">
        <section className="input-section">
          <div className="toggle-buttons">
            <button className={`btn ${showForm ? 'active' : ''}`} onClick={() => dispatch(toggleView())}>
              Form View
            </button>
            <button className={`btn ${showChat ? 'active' : ''}`} onClick={() => dispatch(toggleView())}>
              Chat View
            </button>
          </div>

          {showForm && <LogInteractionForm />}
          {showChat && <ChatInterface />}
        </section>

        <section className="list-section">
          <h2>Recent Interactions</h2>
          <InteractionList interactions={interactions} />
        </section>
      </main>
    </div>
  );
}

export default App;
