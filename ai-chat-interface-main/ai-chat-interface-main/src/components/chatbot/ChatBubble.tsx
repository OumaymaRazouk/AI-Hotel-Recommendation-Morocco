import { Bot, User } from "lucide-react";
import { cn } from "@/lib/utils";
import { Place } from "@/data/places";
import PlaceCard from "./PlaceCard";

interface ChatBubbleProps {
  content: string;
  role: "user" | "assistant";
  isLoading?: boolean;
  places?: Place[];
}

const ChatBubble = ({ content, role, isLoading, places }: ChatBubbleProps) => {
  const isUser = role === "user";

  return (
    <div
      className={cn(
        "flex gap-3 animate-slide-up",
        isUser ? "flex-row-reverse" : "flex-row"
      )}
    >
      {/* Avatar */}
      <div
        className={cn(
          "flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center shadow-sm",
          isUser
            ? "bg-primary text-primary-foreground"
            : "bg-accent text-accent-foreground"
        )}
      >
        {isUser ? (
          <User className="w-5 h-5" />
        ) : (
          <Bot className="w-5 h-5" />
        )}
      </div>

      {/* Message Content */}
      <div className={cn("max-w-[85%] md:max-w-[75%]", isUser && "text-right")}>
        <div
          className={cn(
            "rounded-2xl px-4 py-3",
            isUser
              ? "chat-bubble-user text-primary-foreground"
              : "chat-bubble-assistant text-foreground"
          )}
        >
          {isLoading ? (
            <div className="typing-indicator flex gap-1.5 py-1 px-1">
              <span className="w-2 h-2 rounded-full bg-muted-foreground/50" />
              <span className="w-2 h-2 rounded-full bg-muted-foreground/50" />
              <span className="w-2 h-2 rounded-full bg-muted-foreground/50" />
            </div>
          ) : (
            <p className="text-sm leading-relaxed whitespace-pre-wrap">{content}</p>
          )}
        </div>

        {/* Place Cards */}
        {places && places.length > 0 && (
          <div className="mt-4 grid gap-4 sm:grid-cols-2">
            {places.map((place, index) => (
              <PlaceCard key={place.id} place={place} index={index} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatBubble;
