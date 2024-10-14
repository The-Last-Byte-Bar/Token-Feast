import React from 'react';
import LaunchButton from './components/LaunchButton';
import BarQuote from './components/BarQuote';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to The Last Byte Bar</h1>
        <h2>Token Flight Launch Pad</h2>
      </header>
      <main>
        <BarQuote />
        <LaunchButton />
      </main>
      <footer>
        <p>© 2024 The Last Byte Bar - Token Flight</p>
      </footer>
    </div>
  );
}

export default App;