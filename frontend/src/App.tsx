import { useState } from 'react'
import './App.css'
import { Button } from "@/components/ui/Button"

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Button> Click me </Button>
    </>
  )
}

export default App
