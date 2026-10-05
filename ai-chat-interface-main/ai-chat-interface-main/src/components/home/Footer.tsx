import { Compass, Heart } from "lucide-react";

const Footer = () => {
  return (
    <footer className="py-12 border-t border-border">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center">
              <Compass className="w-4 h-4 text-primary" />
            </div>
            <span className="font-heading font-semibold gradient-text">
              ExploreSmart
            </span>
          </div>

          <p className="text-sm text-muted-foreground flex items-center gap-1">
            Fait avec <Heart className="w-4 h-4 text-destructive fill-destructive" /> pour les voyageurs
          </p>

          <p className="text-sm text-muted-foreground">
            © {new Date().getFullYear()} ExploreSmart. Tous droits réservés.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
