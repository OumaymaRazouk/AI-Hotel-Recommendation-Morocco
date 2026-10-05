import { Link } from "react-router-dom";
import { MessageCircle, ArrowRight } from "lucide-react";

const CTA = () => {
  return (
    <section className="py-20 md:py-32">
      <div className="container mx-auto px-4">
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primary via-ocean to-primary p-8 md:p-16">
          {/* Background Pattern */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute top-0 left-0 w-full h-full" 
              style={{
                backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
              }}
            />
          </div>

          <div className="relative z-10 text-center text-white">
            <h2 className="font-heading text-3xl md:text-5xl font-bold mb-6">
              Prêt à explorer ?
            </h2>
            <p className="text-lg md:text-xl opacity-90 max-w-2xl mx-auto mb-8">
              Commencez dès maintenant à discuter avec notre assistant et 
              découvrez les meilleures destinations adaptées à vos envies.
            </p>
            <Link
              to="/chatbot"
              className="inline-flex items-center gap-3 px-8 py-4 rounded-full bg-white text-primary font-semibold text-lg hover:bg-white/90 transition-all hover:scale-105 shadow-lg"
            >
              <MessageCircle className="w-5 h-5" />
              Lancer le chatbot
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CTA;
