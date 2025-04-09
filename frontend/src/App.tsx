import { useState } from 'react'
import { Loader2 } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

import './App.css'

enum Status { idle, submitting, success, error }

function App() {
  const [review, setReview] = useState<string>('')
  const [score, setScore] = useState<number>(0)
  const [error, setError] = useState<string>('No further infomation')
  const [status, setStatus] = useState<Status>(Status.idle)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!review.trim()) return; // 空内容不提交

    setStatus(Status.submitting);

    fetch('/api/score', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ review }),
    }).then((response) => {
      if (!response.ok) {
        throw new Error(`Request failed with code ${response.status}`);
      }
      return response.json()
    }).then((data) => {
      setScore(data.score)
      setStatus(Status.success)
    }).catch((err) => {
      setError(err instanceof Error ? err.message : 'Unknown error');
      setStatus(Status.error);
    })
  }

  return (
    <>
      <form
        onSubmit={handleSubmit}
        className="flex w-full max-w-sm items-center space-x-2"
      >
        {/* TODO: turn to textarea  */}
        <Input
          type="text"
          value={review}
          onChange={(e) => setReview(e.target.value)}
          placeholder="Input your review here"
          disabled={status === Status.submitting}
        />
        <Button
          disabled={status === Status.submitting}
          className="w-30"
        >
          {status !== Status.submitting ?
            <> Get Score </>
            :
            <> <Loader2 className="animate-spin" /> Please wait </>
          }
        </Button>
      </form>

      {status === Status.submitting && (
        <p className="text-base font-mono">Caculating your score...</p>
      )}

      {status === Status.success && (
        <p className="text-base font-mono">Your score is: {score.toFixed(2)}</p>
      )}

      {status === Status.error && (
        <div className="text-base font-mono">
          <p className="text-red-400 font-bold">Oops, something went wrong.</p>
          {error}
        </div>
      )}
    </>
  )
}

export default App
