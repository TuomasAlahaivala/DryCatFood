import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from 'react'
import Table from "./components/table";

function App() {
  const [nutritional_values, setNutritionalValues] = useState([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    setIsLoading(true);
    fetch("/api/ml").then(function (res) {
          return res.json();
    }).then(function(data) {
        setNutritionalValues(data.nutritional_values)
        setIsLoading(false);
    })
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        {isLoading ? <p>Lataa...</p> : <Table data={nutritional_values} />}
      </header>
    </div>
  );
}

export default App;
