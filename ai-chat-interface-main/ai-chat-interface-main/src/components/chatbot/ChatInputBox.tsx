import { useState, KeyboardEvent } from "react";
import { Send, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";

interface ChatInputBoxProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

const ChatInputBox = ({ onSend, disabled }: ChatInputBoxProps) => {
  const [message, setMessage] = useState("");

  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSend(message.trim());
      setMessage("");
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="bg-card rounded-2xl border border-border p-4 shadow-lg">
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Décrivez le type de lieu que vous cherchez..."
        disabled={disabled}
        rows={3}
        className={cn(
          "w-full resize-none rounded-xl border border-border bg-muted/50 px-4 py-3 text-sm",
          "placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary",
          "transition-all duration-200",
          disabled && "opacity-50 cursor-not-allowed"
        )}
      />

      <div className="flex items-center justify-between mt-3">
        <p className="text-xs text-muted-foreground flex items-center gap-1.5">
          <Sparkles className="w-3 h-3" />
          Entrée pour envoyer • Shift+Entrée pour sauter une ligne
        </p>

        <button
          onClick={handleSend}
          disabled={!message.trim() || disabled}
          className={cn(
            "btn-primary inline-flex items-center gap-2 px-5 py-2.5 rounded-full text-sm font-semibold text-primary-foreground",
            "disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-none"
          )}
        >
          <Send className="w-4 h-4" />
          Envoyer
        </button>
      </div>
    </div>
  );
};

export default ChatInputBox;
