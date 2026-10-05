import { useState, useRef, useEffect } from "react";
import { Bot, Sparkles } from "lucide-react";
import ChatBubble from "./ChatBubble";
import ChatInputBox from "./ChatInputBox";
import QuickSuggestions from "./QuickSuggestions";
import { Place, searchPlaces } from "@/data/places";

interface Message {
  id: string;
  content: string;
  role: "user" | "assistant";
  places?: Place[];
}

const INITIAL_MESSAGE: Message = {
  id: "1",
  content: "Bonjour ! 👋 Je suis votre assistant ExploreSmart. Dites-moi ce que vous recherchez : plages, désert, montagnes, culture, aventure... Je vous recommanderai les meilleurs endroits au Maroc !",
  role: "assistant",
};

const QUICK_SUGGESTIONS = [
  "Plages à Agadir",
  "Désert et dunes",
  "Sites historiques",
  "Villes bleues",
  "Nature et cascades",
];

const RECOMMENDATION_KEYWORDS = [
  "plage", "mer", "océan", "désert", "dune", "montagne", "cascade",
  "médina", "culture", "histoire", "randonnée", "nature", "aventure",
  "surf", "ville", "jardin", "kasbah", "lagune", "souk", "artisanat",
  "recommande", "suggère", "propose", "cherche", "trouve", "visite"
];

const ChatbotContainer = () => {
  const [messages, setMessages] = useState<Message[]>([INITIAL_MESSAGE]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const shouldRecommend = (text: string): boolean => {
    const lowerText = text.toLowerCase();
    return RECOMMENDATION_KEYWORDS.some((keyword) =>
      lowerText.includes(keyword)
    );
  };

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: "user",
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    // Simulate AI processing
    await new Promise((resolve) => setTimeout(resolve, 1200));

    let response: Message;

    if (shouldRecommend(content)) {
      const places = searchPlaces(content, 4);
      
      if (places.length > 0) {
        response = {
          id: (Date.now() + 1).toString(),
          content: `Parfait ! 🌟 J'ai trouvé ${places.length} destinations qui correspondent à votre recherche. Voici mes recommandations :`,
          role: "assistant",
          places,
        };
      } else {
        response = {
          id: (Date.now() + 1).toString(),
          content: "Je n'ai pas trouvé de destination correspondant exactement à votre recherche. Essayez des termes comme : plage, désert, montagne, médina, culture, nature, ou mentionnez une ville comme Marrakech, Agadir, Fès...",
          role: "assistant",
        };
      }
    } else {
      // Generic FAQ responses
      const responses = [
        "Je suis là pour vous aider à trouver les meilleures destinations au Maroc ! Dites-moi quel type d'expérience vous recherchez : détente à la plage, aventure dans le désert, exploration culturelle... 🌍",
        "Qu'aimeriez-vous découvrir au Maroc ? Je peux vous suggérer des plages magnifiques, des sites historiques, des paysages désertiques ou des villes pittoresques. 🏖️🏜️🏔️",
        "N'hésitez pas à me décrire vos envies ! Par exemple : « Je cherche des plages tranquilles » ou « Recommande-moi des endroits pour la randonnée ». Je suis là pour vous guider ! 🧭",
      ];
      
      response = {
        id: (Date.now() + 1).toString(),
        content: responses[Math.floor(Math.random() * responses.length)],
        role: "assistant",
      };
    }

    setMessages((prev) => [...prev, response]);
    setIsLoading(false);
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="px-6 py-4 border-b border-border bg-card/50 backdrop-blur-sm rounded-t-2xl">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-xl bg-accent/20 flex items-center justify-center">
            <Bot className="w-6 h-6 text-accent" />
          </div>
          <div>
            <h2 className="font-heading font-semibold text-lg">Assistant ExploreSmart</h2>
            <p className="text-xs text-muted-foreground flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-accent animate-pulse" />
              En ligne • Prêt à vous aider
            </p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((message) => (
          <ChatBubble
            key={message.id}
            content={message.content}
            role={message.role}
            places={message.places}
          />
        ))}
        {isLoading && (
          <ChatBubble content="" role="assistant" isLoading />
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Suggestions */}
      {messages.length <= 2 && !isLoading && (
        <div className="px-6 pb-4">
          <p className="text-xs text-muted-foreground mb-2 flex items-center gap-1.5">
            <Sparkles className="w-3 h-3" />
            Suggestions rapides
          </p>
          <QuickSuggestions
            suggestions={QUICK_SUGGESTIONS}
            onSelect={handleSendMessage}
          />
        </div>
      )}

      {/* Input */}
      <div className="p-4 border-t border-border bg-background/80 backdrop-blur-sm rounded-b-2xl">
        <ChatInputBox onSend={handleSendMessage} disabled={isLoading} />
      </div>
    </div>
  );
};

export default ChatbotContainer;
