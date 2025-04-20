import ShortenForm from "@/components/ShortenForm";
import Image from "next/image";

export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="container mx-auto flex flex-col md:flex-row items-stretch">
        
        {/* Left: Form Section with Background Image */}
        <div className="md:w-2/5 h-screen relative flex items-center justify-center">
          <Image
            src="/left-img.webp"
            alt="Background for form"
            fill
            className="object-cover absolute z-0"
          />
          <div className="relative w-full m-4">
            <ShortenForm />
          </div>
        </div>

        {/* Right: Full-height Hero Image */}
        <div className="md:w-3/5 h-screen relative bg-black">
          <Image
            src="/hero-img.jfif"
            alt="Shorten your URLs easily"
            fill
            className="object-cover rounded-lg shadow-lg"
          />
        </div>

      </div>
    </main>
  );
}
