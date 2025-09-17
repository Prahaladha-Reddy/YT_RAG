import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <div className='p-4 w-64'>
      <div className="text-6xl text-blue-900 font-bold">
        "React Chrome Extension"
      </div>
      <p>Counter: {count}</p>
      <button
      className="bg-blue-500 text-white px-3 py-1 rounded"
      onClick={()=>setCount(count+1)}
      >
        Play
      </button>
    </div>
    </>
  )
}

export default App
