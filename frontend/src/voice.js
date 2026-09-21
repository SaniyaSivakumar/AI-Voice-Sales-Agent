// Web Speech API Voice Recognition & Synthesis Manager

export class VoiceEngine {
  constructor(onResultCallback, onStateChangeCallback) {
    this.recognition = null;
    this.synthesis = window.speechSynthesis || null;
    this.isListening = false;
    this.onResult = onResultCallback;
    this.onStateChange = onStateChangeCallback;

    this.initRecognition();
  }

  initRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      console.warn("Web Speech Recognition API is not supported in this browser environment.");
      return;
    }

    this.recognition = new SpeechRecognition();
    this.recognition.continuous = true;
    this.recognition.interimResults = true;
    this.recognition.lang = "en-US";

    this.recognition.onstart = () => {
      this.isListening = true;
      if (this.onStateChange) this.onStateChange("listening");
    };

    this.recognition.onend = () => {
      this.isListening = false;
      if (this.onStateChange) this.onStateChange("idle");
    };

    this.recognition.onerror = (event) => {
      console.error("Speech Recognition Error:", event.error);
      this.isListening = false;
      if (this.onStateChange) this.onStateChange("error", event.error);
    };

    this.recognition.onresult = (event) => {
      let finalTranscript = "";
      let interimTranscript = "";

      for (let i = event.resultIndex; i < event.results.length; ++i) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript;
        } else {
          interimTranscript += transcript;
        }
      }

      if (this.onResult) {
        this.onResult({
          final: finalTranscript.trim(),
          interim: interimTranscript.trim()
        });
      }
    };
  }

  startListening() {
    if (this.recognition && !this.isListening) {
      try {
        this.recognition.start();
      } catch (err) {
        console.error("Failed to start speech recognition:", err);
      }
    }
  }

  stopListening() {
    if (this.recognition && this.isListening) {
      try {
        this.recognition.stop();
      } catch (err) {
        console.error("Failed to stop speech recognition:", err);
      }
    }
  }

  speak(text, onEndCallback) {
    if (!this.synthesis) {
      if (onEndCallback) onEndCallback();
      return;
    }

    // Cancel any ongoing speech
    this.synthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.lang = "en-US";

    if (this.onStateChange) this.onStateChange("speaking");

    utterance.onend = () => {
      if (this.onStateChange) this.onStateChange("idle");
      if (onEndCallback) onEndCallback();
    };

    utterance.onerror = (err) => {
      console.warn("Speech Synthesis Warning/Error:", err);
      if (this.onStateChange) this.onStateChange("idle");
      if (onEndCallback) onEndCallback();
    };

    this.synthesis.speak(utterance);
  }
}

/**
 * Classifies raw user text into sales intents (Fallback client-side classifier)
 * Ready to be connected to Padma's Deep Learning model!
 */
export function detectLocalIntent(text) {
  const lower = text.toLowerCase();

  if (/\b(hello|hi|hey|good morning|good evening|greetings)\b/.test(lower)) {
    return { intent: "greeting", confidence: 0.95 };
  }
  if (/\b(bye|goodbye|see you|thanks|thank you)\b/.test(lower)) {
    return { intent: "goodbye", confidence: 0.95 };
  }
  if (/\b(recommend|suggest|best|top|popular)\b/.test(lower)) {
    return { intent: "product_recommendation", confidence: 0.9 };
  }
  if (/\b(price|cost|how much|rate|expensive|cheap|dollars)\b/.test(lower)) {
    return { intent: "price_query", confidence: 0.9 };
  }
  if (/\b(discount|sale|deal|offer|coupon|promo|code)\b/.test(lower)) {
    return { intent: "discount_query", confidence: 0.9 };
  }
  if (/\b(stock|available|in stock|out of stock|quantity|have)\b/.test(lower)) {
    return { intent: "availability", confidence: 0.9 };
  }
  if (/\b(feature|spec|specification|battery|display|waterproof|screen|ram|gb|storage)\b/.test(lower)) {
    return { intent: "feature_query", confidence: 0.85 };
  }
  
  // Default to product search
  return { intent: "product_search", confidence: 0.8 };
}
