import Navbar from "@/components/home/Navbar";
import Hero from "@/components/home/Hero";
import Features from "@/components/home/Features";
import Audience from "@/components/home/Audience";
import CTA from "@/components/home/CTA";
import Footer from "@/components/home/Footer";

const Index = () => {
  return (
    <div className="min-h-screen">
      <Navbar />
      <Hero />
      <Features />
      <Audience />
      <CTA />
      <Footer />
    </div>
  );
};

export default Index;
