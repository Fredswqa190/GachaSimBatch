"use client";

import { useState, useEffect } from 'react';
import Image from 'next/image';

type Characters = {
  [key: number]: number;
};

const Gacha = () => {
  const [wishes, setWishes] = useState(100);
  const [time, setTime] = useState(1200);
  const [characters, setCharacters] = useState<Characters>({
    1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0
  });
  const [error, setError] = useState('');
  const [view, setView] = useState('start'); // 'start', 'main', 'history', 'rules', 'results'
  const [results, setResults] = useState<number[]>([]);
  const [loading, setLoading] = useState(false);

  const charNames: { [key: number]: string } = {
    1: "Sienna Ines", // 1 5-star 
    2: "Raziel Sera", 3: "Styx Ferryman", // 2 4-star characters
    4: "Lost Sea of Polaris", 5: "Hydra of Lerna", 6: "Seraphim's Tome", 7: "Beacon of Splendor", // 4 3-star weapons
    8: "Whiplash", 9: "Swordfish", 10: "Cerulean", 11: "Charybdis" // 4 2-star weapons
  };

  useEffect(() => {
    if (time > 0 && view === 'main') {
      const timer = setTimeout(() => setTime(time - 1), 1000);
      return () => clearTimeout(timer);
    } else if (time === 0) {
      setError("Time's up! Game over.");
      setView('start');
    }
  }, [time, view]);

  const randNum = () => {
    const star = Math.floor(Math.random() * 100) + 1;
    if (star >= 1 && star <= 2) return 1;
    if (star >= 3 && star <= 12) return Math.floor(Math.random() * 2) + 2;
    if (star >= 13 && star <= 50) return Math.floor(Math.random() * 4) + 4;
    return Math.floor(Math.random() * 4) + 8;
  };

  const rollOne = () => {
    if (wishes === 0 || time === 0) {
      setError("Can't wish anymore.");
      setTimeout(() => setError(''), 3000);
      return;
    }
    setLoading(true);
    setTimeout(() => {
      const num = randNum();
      setWishes(wishes - 1);
      setCharacters(prev => ({ ...prev, [num]: prev[num] + 1 }));
      setResults([num]);
      setView('results');
      setLoading(false);
    }, 4800); 
  };

  const rollTen = () => {
    if (wishes < 10 || time === 0) {
      setError("Can't wish anymore.");
      setTimeout(() => setError(''), 3000);
      return;
    }
    setLoading(true);
    setTimeout(() => {
      const nums: number[] = [];
      for (let i = 0; i < 10; i++) {
        const num = randNum();
        nums.push(num);
        setWishes(prev => prev - 1);
        setCharacters(prev => ({ ...prev, [num]: prev[num] + 1 }));
      }
      setResults(nums);
      setView('results');
      setLoading(false);
    }, 4800); 
  };

  const displayHistory = () => {
    setView('history');
  };

  const displayRules = () => {
    setView('rules');
  };

  const quit = () => {
    setWishes(100);
    setTime(1200);
    setCharacters({
      1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0
    });
    setView('main');
  };

  const mainMenu = () => {
    setView('main');
  };

  const startGame = () => {
    setView('main');
  };

  return (
    <div className="container">
      <main>
        {!loading && view === 'start' && (
          <>
            <div className="full-size-image">
              <Image src="/start.png" alt="Start Screen" layout="fill" objectFit="cover" />
            </div>
            <div className="content">
              <h1>Gacha Simulator</h1>
              <p>You will have 100 wishes and 20 minutes to get a character</p>
              <button className="btn" onClick={startGame}>Start</button>
            </div>
          </>
        )}
        {!loading && view === 'main' && (
          <>
            <div className="full-size-image">
              <Image src="/mainmenu.gif" alt="Main Menu" layout="fill" objectFit="cover" unoptimized />
            </div>
            <div className="content">
              <h1>Gacha Simulator</h1>
              <p>You will have 100 wishes and 20 minutes to get a character</p>
              <div className="buttons">
                <button className="btn" onClick={rollOne}>1 Pull</button>
                <button className="btn" onClick={rollTen}>10 Pull</button>
                <button className="btn" onClick={displayHistory}>History</button>
                <button className="btn" onClick={displayRules}>Rules</button>
                <button className="btn" onClick={quit}>Quit</button>
              </div>
              <p>{error}</p>
              <p>Remaining wishes: {wishes}</p>
              <p>Timer: {Math.floor(time / 60)} minutes {time % 60} seconds</p>
            </div>
          </>
        )}
        {!loading && view === 'history' && (
          <>
            <div className="full-size-image">
              <Image src="/background.gif" alt="Background" layout="fill" objectFit="cover" unoptimized />
            </div>
            <div className="content">
              <h2>History</h2>
              <div className="history">
                <h3>Characters</h3>
                <ul>
                  {Object.keys(characters).slice(0, 3).map(key => (
                    <li key={key}>{`${charNames[Number(key)]}: ${characters[Number(key)]}`}</li>
                  ))}
                </ul>
                <h3>Weapons</h3>
                <ul>
                  {Object.keys(characters).slice(3).map(key => (
                    <li key={key}>{`${charNames[Number(key)]}: ${characters[Number(key)]}`}</li>
                  ))}
                </ul>
              </div>
              <button className="btn" onClick={mainMenu}>Main Menu</button>
            </div>
          </>
        )}
        {!loading && view === 'rules' && (
          <>
            <div className="full-size-image">
              <Image src="/background.gif" alt="Background" layout="fill" objectFit="cover" unoptimized />
            </div>
            <div className="content">
              <h2>Rules</h2>
              <p>Rate Rules and Details:</p>
              <ul>
                <li>Basic rate of summoning 5☆ characters: 2%</li>
                <li>Basic rate of summoning 4☆ characters: 10%</li>
                <li>Basic rate of summoning 3☆ weapons: 38%</li>
                <li>Basic rate of summoning 2☆ weapons: 50%</li>
              </ul>
              <p>Time-limited summoning event has begun. During the event, there will be no rate-ups, no guarantee counters, or a pity system that affect the rates; all base rates will be permanent for the duration of the event. The basic rate applies to all characters. Each Summon x10 will consume 10,000 gems.</p>
              <button className="btn" onClick={mainMenu}>Main Menu</button>
            </div>
          </>
        )}
        {!loading && view === 'results' && (
          <>
            <div className="content">
              <h2>Results</h2>
              <div className="results">
                {results.map((num, index) => (
                  <div key={index}>
                    <Image src={`/${num}.jpg`} alt={charNames[num]} width={100} height={200} />
                    <p>{charNames[num]}</p>
                  </div>
                ))}
              </div>
              <button className="btn" onClick={mainMenu}>Main Menu</button>
            </div>
          </>
        )}
        {loading && (
          <div className="loading">
            <Image src="/wish.gif" alt="Loading..." layout="fill" objectFit="cover" />
          </div>
        )}
      </main>
      <style jsx>{`
        .container {
          text-align: center;
          position: relative;
          width: 100%;
          height: 100vh;
          display: flex;
          justify-content: center;
          align-items: center;
          font-family: 'Roboto', sans-serif;
        }
        .content {
          position: relative;
          z-index: 1;
          background: rgba(255, 255, 255, 0.8);
          padding: 20px;
          border-radius: 10px;
          color: black; 
          margin-top: -20px; 
        }
        .content h1 {
          color: black; 
          font-size: 3em; 
          margin-top: -20px; 
        }
        .buttons {
          margin: 20px;
        }
        .btn {
          background-color: #0070f3;
          border: none;
          color: white;
          padding: 10px 20px;
          text-align: center;
          text-decoration: none;
          display: inline-block;
          font-size: 16px;
          margin: 4px 2px;
          cursor: pointer;
          border-radius: 5px;
          transition: background-color 0.3s ease;
        }
        .btn:hover {
          background-color: #005bb5;
        }
        .results {
          display: flex;
          justify-content: center;
          flex-wrap: wrap;
        }
        .results div {
          margin: 10px;
        }
        .loading {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          z-index: 10;
        }
        .full-size-image {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          z-index: -1;
        }
      `}</style>
    </div>
  );
};

export default Gacha;