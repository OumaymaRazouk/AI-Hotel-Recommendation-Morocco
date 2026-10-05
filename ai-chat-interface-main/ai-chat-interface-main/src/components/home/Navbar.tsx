import { Link } from "react-router-dom";
import { Compass, MessageCircle, Menu, X } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border/50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center group-hover:bg-primary/20 transition-colors">
              <Compass className="w-5 h-5 text-primary" />
            </div>
            <span className="font-heading font-bold text-xl gradient-text">
              ExploreSmart
            </span>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden md:flex items-center gap-6">
            <Link
              to="/"
              className="text-muted-foreground hover:text-foreground transition-colors text-sm font-medium"
            >
              Accueil
            </Link>
            <Link
              to="/chatbot"
              className="btn-primary inline-flex items-center gap-2 px-5 py-2.5 rounded-full text-sm font-semibold text-primary-foreground"
            >
              <MessageCircle className="w-4 h-4" />
              Tester le chatbot
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 rounded-lg hover:bg-muted transition-colors"
          >
            {isOpen ? (
              <X className="w-6 h-6" />
            ) : (
              <Menu className="w-6 h-6" />
            )}
          </button>
        </div>

        {/* Mobile Nav */}
        <div
          className={cn(
            "md:hidden overflow-hidden transition-all duration-300",
            isOpen ? "max-h-48 pb-4" : "max-h-0"
          )}
        >
          <div className="flex flex-col gap-3 pt-2">
            <Link
              to="/"
              onClick={() => setIsOpen(false)}
              className="px-4 py-2 rounded-lg hover:bg-muted transition-colors"
            >
              Accueil
            </Link>
            <Link
              to="/chatbot"
              onClick={() => setIsOpen(false)}
              className="btn-primary inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-full text-sm font-semibold text-primary-foreground"
            >
              <MessageCircle className="w-4 h-4" />
              Tester le chatbot
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
