"use client";

import {
  useEffect,
  useRef,
  useState,
  startTransition,
  type FormEvent,
} from "react";

import useAuth from "@/hooks/useAuth";
import DashboardLayout from "@/components/dashboard/DashboardLayout";

import {
  Bot,
  BriefcaseBusiness,
  FileText,
  Loader2,
  MessageSquareText,
  Send,
  Sparkles,
  Target,
  Trash2,
  User,
} from "lucide-react";

import {
  sendChatMessage,
  type ChatContext,
} from "@/lib/api";


interface ChatMessage {
  id: number;
  role: "user" | "assistant";
  content: string;
  contextUsed?: ChatContext[];
}


const SUGGESTED_PROMPTS = [
  {
    label: "Resume",
    icon: FileText,
    message:
      "What are the strongest skills on my resume?",
  },
  {
    label: "ATS",
    icon: Target,
    message:
      "Why could my ATS score be improved?",
  },
  {
    label: "Job Match",
    icon: BriefcaseBusiness,
    message:
      "What skills am I missing for the job I matched against?",
  },
  {
    label: "Interview",
    icon: MessageSquareText,
    message:
      "How did I perform in my mock interview?",
  },
];


const CONTEXT_LABELS: Record<
  ChatContext,
  string
> = {
  resume: "Resume",
  ats_analysis: "ATS Analysis",
  job_match: "Job Match",
  interview: "Interview",
};


export default function ChatPage() {
  const {
    token,
    user,
    isAuthenticated,
    isLoading: authLoading,
  } = useAuth();

  const [messages, setMessages] =
    useState<ChatMessage[]>([]);

  const [input, setInput] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const messagesEndRef =
    useRef<HTMLDivElement | null>(null);
  const loadedUserIdRef =
    useRef<number | null>(null);


  /*
   * =========================================================
   * Chat History Persistence
   * =========================================================
   *
   * Each authenticated user gets their own localStorage key.
   *
   * Example:
   *
   * interviewpilot_chat_9
   *
   * This prevents one user's chat history from appearing
   * for another user on the same browser.
   */

  useEffect(() => {
    loadedUserIdRef.current = null;
    startTransition(() => {
      setMessages([]);
    });

    if (!user) {
      return;
    }

    const storageKey =
      `interviewpilot_chat_${user.id}`;

    const savedMessages =
      localStorage.getItem(storageKey);

      if (!savedMessages) {
        loadedUserIdRef.current = user.id;
        return;
      }

    try {
      const parsed =
        JSON.parse(savedMessages);

      if (!Array.isArray(parsed)) {
        localStorage.removeItem(storageKey);
        loadedUserIdRef.current = user.id;
        return;
      }

      /*
       * Basic validation before restoring the messages.
       * This prevents malformed localStorage data from
       * breaking the chat UI.
       */

      const validMessages =
        parsed.filter(
          (message): message is ChatMessage => {
            return (
              message !== null &&
              typeof message === "object" &&
              typeof message.id === "number" &&
              (
                message.role === "user" ||
                message.role === "assistant"
              ) &&
              typeof message.content === "string"
            );
          }
        );

      setMessages(validMessages);
      loadedUserIdRef.current = user.id;
    } catch (err) {
      console.error(
        "Failed to restore chat history:",
        err
      );

      localStorage.removeItem(
        storageKey
      );
      loadedUserIdRef.current = user.id;
    }
  }, [user]);


  /*
   * Save chat history whenever the message list changes.
   */

  useEffect(() => {
    if (
      !user ||
      loadedUserIdRef.current !== user.id ||
      messages.length === 0
    ) {
      return;
    }

    const storageKey =
      `interviewpilot_chat_${user.id}`;

    try {
      localStorage.setItem(
        storageKey,
        JSON.stringify(messages)
      );
    } catch (err) {
      console.error(
        "Failed to save chat history:",
        err
      );
    }
  }, [messages, user]);


  /*
   * Automatically scroll to the newest message.
   */

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);


  async function handleSend(
    event?: FormEvent
  ) {
    event?.preventDefault();

    const message = input.trim();

    if (!message || loading) {
      return;
    }

    if (!isAuthenticated || !token) {
      setError(
        "Your session has expired. Please log in again."
      );
      return;
    }

    const userMessage: ChatMessage = {
      id: Date.now(),
      role: "user",
      content: message,
    };

    setMessages((previous) => [
      ...previous,
      userMessage,
    ]);

    setInput("");
    setError(null);
    setLoading(true);

    try {
      const response =
        await sendChatMessage(
          message,
          token
        );

      const assistantMessage: ChatMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: response.reply,
        contextUsed:
          response.context_used,
      };

      setMessages((previous) => [
        ...previous,
        assistantMessage,
      ]);
    } catch (err) {
      console.error(
        "Chat request failed:",
        err
      );

      setError(
        err instanceof Error
          ? err.message
          : "Failed to send message."
      );
    } finally {
      setLoading(false);
    }
  }


  function setSuggestedPrompt(
    message: string
  ) {
    setInput(message);
  }


  function clearChat() {
    if (!user) {
      return;
    }

    const storageKey =
      `interviewpilot_chat_${user.id}`;

    localStorage.removeItem(
      storageKey
    );

    setMessages([]);
    setInput("");
    setError(null);
  }


  if (authLoading) {
    return (
      <DashboardLayout>
        <div className="flex min-h-[70vh] items-center justify-center">
          <div className="flex items-center gap-3 text-sm text-slate-400">
            <Loader2
              size={18}
              className="animate-spin text-blue-400"
            />
            Checking your session...
          </div>
        </div>
      </DashboardLayout>
    );
  }


  if (!isAuthenticated) {
    return (
      <DashboardLayout>
        <div className="flex min-h-[70vh] items-center justify-center px-6">
          <div className="w-full max-w-2xl rounded-3xl border border-slate-800 bg-slate-900/80 p-8 text-center">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-500/10 text-blue-400">
              <Bot size={26} />
            </div>

            <h1 className="mt-5 text-2xl font-bold text-white">
              Login required
            </h1>

            <p className="mt-2 text-sm leading-6 text-slate-400">
              Please log in before using the AI
              assistant.
            </p>
          </div>
        </div>
      </DashboardLayout>
    );
  }


  return (
    <DashboardLayout>
      <main className="flex min-h-[calc(100vh-3rem)] flex-col px-4 py-6 text-white sm:px-6 lg:px-8">
        <div className="mx-auto flex w-full max-w-6xl flex-1 flex-col">

          {/* =====================================================
              Header
          ====================================================== */}

          <header className="mb-6">
            <div className="flex items-start justify-between gap-4">

              <div className="flex items-start gap-4">

                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl border border-blue-500/20 bg-blue-500/10 text-blue-400">
                  <Bot size={23} />
                </div>

                <div>
                  <p className="text-xs font-medium uppercase tracking-[0.22em] text-blue-400">
                    InterviewPilot AI
                  </p>

                  <h1 className="mt-1 text-3xl font-bold tracking-tight text-white sm:text-4xl">
                    AI Assistant
                  </h1>

                  <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400 sm:text-base">
                    Ask questions about your resume,
                    ATS performance, job matches, or
                    interview results.
                  </p>
                </div>

              </div>


              {/* Clear Chat */}

              {messages.length > 0 && (
                <button
                  type="button"
                  onClick={clearChat}
                  disabled={loading}
                  className="flex shrink-0 items-center gap-2 rounded-xl border border-slate-800 bg-slate-900/70 px-3 py-2 text-xs font-medium text-slate-500 transition hover:border-red-500/20 hover:bg-red-500/5 hover:text-red-400 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <Trash2 size={15} />
                  <span className="hidden sm:inline">
                    Clear Chat
                  </span>
                </button>
              )}

            </div>
          </header>


          {/* =====================================================
              Chat Container
          ====================================================== */}

          <div className="flex flex-1 flex-col overflow-hidden rounded-3xl border border-slate-800 bg-slate-900/70 shadow-2xl">

            {/* ===================================================
                Messages
            ==================================================== */}

            <div className="flex-1 overflow-y-auto p-5 sm:p-7">

              {messages.length === 0 ? (
                <div className="flex min-h-[55vh] flex-col items-center justify-center text-center">

                  <div className="flex h-16 w-16 items-center justify-center rounded-2xl border border-blue-500/20 bg-blue-500/10 text-blue-400">
                    <Sparkles size={28} />
                  </div>

                  <h2 className="mt-6 text-2xl font-semibold text-white">
                    How can I help?
                  </h2>

                  <p className="mt-2 max-w-lg text-sm leading-6 text-slate-500">
                    Ask naturally. You don&apos;t need to choose
                    whether your question is about your resume,
                    ATS, job match, or interview.
                  </p>

                  <div className="mt-8 grid w-full max-w-3xl gap-3 sm:grid-cols-2">

                    {SUGGESTED_PROMPTS.map(
                      (prompt) => {
                        const Icon =
                          prompt.icon;

                        return (
                          <button
                            key={prompt.label}
                            type="button"
                            onClick={() =>
                              setSuggestedPrompt(
                                prompt.message
                              )
                            }
                            className="group rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-left transition hover:border-blue-500/30 hover:bg-blue-500/5"
                          >
                            <div className="flex items-start gap-3">

                              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
                                <Icon size={18} />
                              </div>

                              <div>
                                <p className="text-sm font-semibold text-white">
                                  {prompt.label}
                                </p>

                                <p className="mt-1 text-sm leading-5 text-slate-500">
                                  {prompt.message}
                                </p>
                              </div>

                            </div>
                          </button>
                        );
                      }
                    )}

                  </div>
                </div>

              ) : (

                <div className="mx-auto max-w-4xl space-y-6">

                  {messages.map(
                    (message) => {
                      const isUser =
                        message.role ===
                        "user";

                      return (
                        <div
                          key={message.id}
                          className={`flex gap-3 ${
                            isUser
                              ? "justify-end"
                              : "justify-start"
                          }`}
                        >

                          {!isUser && (
                            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
                              <Bot size={17} />
                            </div>
                          )}

                          <div className="max-w-[85%]">

                            <div
                              className={`rounded-2xl px-4 py-3.5 text-sm leading-7 ${
                                isUser
                                  ? "rounded-br-md bg-blue-600 text-white"
                                  : "rounded-bl-md border border-slate-800 bg-slate-950/70 text-slate-300"
                              }`}
                            >
                              {message.content}
                            </div>

                            {!isUser &&
                              message.contextUsed &&
                              message.contextUsed.length >
                                0 && (
                                <div className="mt-2 flex flex-wrap gap-2">

                                  {message.contextUsed.map(
                                    (context) => (
                                      <span
                                        key={context}
                                        className="rounded-full border border-slate-800 bg-slate-900 px-2.5 py-1 text-[11px] text-slate-500"
                                      >
                                        Based on{" "}
                                        {CONTEXT_LABELS[
                                          context
                                        ]}
                                      </span>
                                    )
                                  )}

                                </div>
                              )}

                          </div>

                          {isUser && (
                            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-800 text-slate-300">
                              <User size={17} />
                            </div>
                          )}

                        </div>
                      );
                    }
                  )}


                  {/* Loading bubble */}

                  {loading && (
                    <div className="flex gap-3">

                      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
                        <Bot size={17} />
                      </div>

                      <div className="rounded-2xl rounded-bl-md border border-slate-800 bg-slate-950/70 px-4 py-3.5">
                        <div className="flex items-center gap-2 text-sm text-slate-500">

                          <Loader2
                            size={15}
                            className="animate-spin text-blue-400"
                          />

                          Thinking...

                        </div>
                      </div>

                    </div>
                  )}

                  <div ref={messagesEndRef} />

                </div>
              )}

            </div>


            {/* ===================================================
                Error
            ==================================================== */}

            {error && (
              <div className="mx-5 mb-3 rounded-2xl border border-red-500/20 bg-red-500/5 px-4 py-3 text-sm text-red-300 sm:mx-7">
                {error}
              </div>
            )}


            {/* ===================================================
                Follow-up Prompts
            ==================================================== */}

            {messages.length > 0 &&
              !loading && (
                <div className="border-t border-slate-800 px-5 py-3 sm:px-7">

                  <div className="flex gap-2 overflow-x-auto pb-1">

                    <button
                      type="button"
                      onClick={() =>
                        setSuggestedPrompt(
                          "What should I improve next?"
                        )
                      }
                      className="shrink-0 rounded-full border border-slate-800 bg-slate-950/60 px-3 py-1.5 text-xs text-slate-400 transition hover:border-blue-500/30 hover:text-blue-300"
                    >
                      What should I improve next?
                    </button>

                    <button
                      type="button"
                      onClick={() =>
                        setSuggestedPrompt(
                          "What are my biggest career gaps?"
                        )
                      }
                      className="shrink-0 rounded-full border border-slate-800 bg-slate-950/60 px-3 py-1.5 text-xs text-slate-400 transition hover:border-blue-500/30 hover:text-blue-300"
                    >
                      What are my biggest career gaps?
                    </button>

                    <button
                      type="button"
                      onClick={() =>
                        setSuggestedPrompt(
                          "How can I prepare better for backend interviews?"
                        )
                      }
                      className="shrink-0 rounded-full border border-slate-800 bg-slate-950/60 px-3 py-1.5 text-xs text-slate-400 transition hover:border-blue-500/30 hover:text-blue-300"
                    >
                      How can I prepare better?
                    </button>

                  </div>

                </div>
              )}


            {/* ===================================================
                Composer
            ==================================================== */}

            <form
              onSubmit={handleSend}
              className="border-t border-slate-800 p-4 sm:p-5"
            >

              <div className="mx-auto flex max-w-4xl items-end gap-3 rounded-2xl border border-slate-700 bg-slate-950/80 p-2 focus-within:border-blue-500/40">

                <textarea
                  value={input}
                  onChange={(event) =>
                    setInput(
                      event.target.value
                    )
                  }
                  onKeyDown={(event) => {
                    if (
                      event.key ===
                        "Enter" &&
                      !event.shiftKey
                    ) {
                      event.preventDefault();
                      handleSend();
                    }
                  }}
                  placeholder="Ask anything about your InterviewPilot progress..."
                  rows={1}
                  className="max-h-36 min-h-12 flex-1 resize-none bg-transparent px-3 py-3 text-sm leading-6 text-white outline-none placeholder:text-slate-600"
                  disabled={loading}
                />

                <button
                  type="submit"
                  disabled={
                    loading ||
                    !input.trim()
                  }
                  aria-label="Send message"
                  className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-blue-600 text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  {loading ? (
                    <Loader2
                      size={18}
                      className="animate-spin"
                    />
                  ) : (
                    <Send size={18} />
                  )}
                </button>

              </div>

              <p className="mx-auto mt-2 max-w-4xl px-2 text-[11px] text-slate-600">
                Press Enter to send · Shift + Enter
                for a new line
              </p>

            </form>

          </div>
        </div>
      </main>
    </DashboardLayout>
  );
}
