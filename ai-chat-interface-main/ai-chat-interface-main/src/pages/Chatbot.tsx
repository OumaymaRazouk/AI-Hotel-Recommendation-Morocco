import { Link } from "react-router-dom";
import { ArrowLeft, Compass } from "lucide-react";
import ChatbotContainer from "@/components/chatbot/ChatbotContainer";

const Chatbot = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-sky-light/50 to-background">
      {/* Simple Header */}
      <header className="border-b border-border bg-background/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center gap-2 group">
              <div className="w-9 h-9 rounded-lg bg-primary/10 flex items-center justify-center">
                <Compass className="w-5 h-5 text-primary" />
              </div>
              <span className="font-heading font-bold text-lg gradient-text hidden sm:block">
                ExploreSmart
              </span>
            </Link>

            <Link
              to="/"
              className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              Retour à l'accueil
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6 md:py-10">
        <div className="max-w-4xl mx-auto">
          {/* Page Title */}
          <div className="text-center mb-6 md:mb-8">
            <h1 className="font-heading text-2xl md:text-3xl font-bold mb-2">
              Chatbot <span className="gradient-text">Recommandations</span>
            </h1>
            <p className="text-muted-foreground">
              Décrivez vos envies et recevez des recommandations personnalisées
            </p>
          </div>

          {/* Chat Container */}
          <div className="bg-card rounded-2xl border border-border shadow-xl overflow-hidden h-[calc(100vh-220px)] min-h-[500px]">
            <ChatbotContainer />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Chatbot;
