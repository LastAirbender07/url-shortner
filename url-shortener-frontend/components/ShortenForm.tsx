"use client";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Clipboard, CheckCircle } from "lucide-react";
import Confetti from "react-confetti";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;
console.log("API URL: ", API_BASE_URL);

export default function ShortenForm() {
  const [longUrl, setLongUrl] = useState("");
  const [shortUrl, setShortUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    setCopied(false);

    try {
      const response = await fetch(`${API_BASE_URL}/shorten`, {
        method: "POST",
        headers: { "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "69420",
         },
        body: JSON.stringify({ long_url: longUrl }),
      });

      if (!response.ok) throw new Error("Failed to shorten URL");

      const data = await response.json();
      setShortUrl(`${API_BASE_URL}/${data.short_url}`);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleCopy() {
    navigator.clipboard.writeText(shortUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 3000);
  }

  return (
    <div className="w-full max-w-xl p-8 bg-white shadow-md rounded-lg">
      <h1 className="text-2xl font-bold mb-4">Shorten Your URL</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          type="url"
          placeholder="Enter a long URL"
          value={longUrl}
          onChange={(e) => setLongUrl(e.target.value)}
          required
        />

        <Button type="submit" disabled={loading} className="w-full">
          {loading ? "Shortening..." : "Shorten URL"}
        </Button>
      </form>

      {error && <p className="text-red-500 mt-2">{error}</p>}

      {shortUrl && (
        <div className="mt-4 p-3 bg-gray-100 rounded-lg flex justify-between items-center space-x-2 relative">
          <div className="overflow-x-auto whitespace-nowrap scrollbar-thin scrollbar-thumb-gray-300 flex-grow px-2">
            <span className="text-blue-600">{shortUrl}</span>
          </div>

          <Button
            variant="outline"
            size="sm"
            onClick={handleCopy}
            className="flex items-center space-x-2 relative"
          >
            {copied ? (
              <CheckCircle className="text-green-500" />
            ) : (
              <Clipboard />
            )}
          </Button>

          {copied && (
            <Confetti
              width={250} // Small width
              height={300} // Small height
              numberOfPieces={150} // Less confetti
              confettiSource={{ x: 0, y: 0, w: 250, h: 400 }}
              gravity={0.15}
              recycle={false} // Stop after effect
            />
          )}
        </div>
      )}
    </div>
  );
}
