"use client";

import {
  useEffect,
  useState,
  type FormEvent,
} from "react";

import useAuth from "@/hooks/useAuth";

import DashboardLayout from "@/components/dashboard/DashboardLayout";

import {
  ArrowRight,
  BriefcaseBusiness,
  CheckCircle2,
  ChevronRight,
  CircleDot,
  Clock3,
  Loader2,
  MessageSquareText,
  RotateCcw,
  Sparkles,
  Target,
  Trophy,
} from "lucide-react";

import {
  evaluateMockInterview,
  getMockInterviewSession,
  startMockInterview,
  submitMockInterviewAnswer,
  type InterviewEvaluation,
  type MockInterviewResponse,
} from "@/lib/api";


type Difficulty = "easy" | "medium" | "hard";

type InterviewState =
  | "setup"
  | "resume-choice"
  | "active"
  | "completed"
  | "results";


const DIFFICULTIES: {
  value: Difficulty;
  label: string;
  description: string;
}[] = [
  {
    value: "easy",
    label: "Easy",
    description: "Core concepts",
  },
  {
    value: "medium",
    label: "Medium",
    description: "Interview standard",
  },
  {
    value: "hard",
    label: "Hard",
    description: "Deep reasoning",
  },
];


const QUESTION_OPTIONS = [3, 5, 7, 10];


function getProgress(
  questionNumber: number,
  totalQuestions: number
) {
  if (totalQuestions <= 0) {
    return 0;
  }

  return Math.min(
    100,
    Math.max(
      0,
      ((questionNumber - 1) / totalQuestions) *
        100
    )
  );
}


export default function InterviewPage() {
  const {
    token,
    isAuthenticated,
    isLoading: authLoading,
  } = useAuth();

  const [state, setState] =
    useState<InterviewState>("setup");

  const [role, setRole] =
    useState("Backend Engineer");

  const [difficulty, setDifficulty] =
    useState<Difficulty>("medium");

  const [questionCount, setQuestionCount] =
    useState(5);

  const [session, setSession] =
    useState<MockInterviewResponse | null>(null);

  const [answer, setAnswer] =
    useState("");

  const [evaluation, setEvaluation] =
    useState<InterviewEvaluation | null>(null);

  const [loading, setLoading] =
    useState(false);

  const [evaluating, setEvaluating] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const [restoring, setRestoring] =
    useState(true);


  /*
   * Check whether an interview session exists.
   *
   * If an active session exists, do not automatically enter it.
   * Give the user the choice to continue or start a new one.
   */
  useEffect(() => {
    if (authLoading) {
      return;
    }

    async function checkExistingSession() {
      const sessionId =
        localStorage.getItem(
          "mock_interview_session_id"
        );

      if (
        !isAuthenticated ||
        !token ||
        !sessionId
      ) {
        setRestoring(false);
        setState("setup");
        return;
      }

      try {
        const existingSession =
          await getMockInterviewSession(
            sessionId,
            token
          );

        setSession(existingSession);

        if (
          existingSession.status ===
          "completed"
        ) {
          localStorage.removeItem(
            "mock_interview_session_id"
          );

          setSession(null);
          setState("setup");
        } else {
          setState("resume-choice");
        }
      } catch (err) {
        console.error(
          "Failed to check existing interview session:",
          err
        );

        localStorage.removeItem(
          "mock_interview_session_id"
        );

        setSession(null);
        setState("setup");
      } finally {
        setRestoring(false);
      }
    }

    checkExistingSession();
  }, [
    authLoading,
    isAuthenticated,
    token,
  ]);


  function continueExistingInterview() {
    if (!session) {
      setError(
        "The existing interview session could not be restored."
      );

      setState("setup");
      return;
    }

    setError(null);
    setAnswer("");
    setState("active");
  }


  function startNewInterview() {
    localStorage.removeItem(
      "mock_interview_session_id"
    );

    setSession(null);
    setEvaluation(null);
    setAnswer("");
    setError(null);
    setEvaluating(false);
    setState("setup");
  }


  async function handleStartInterview(
    event: FormEvent
  ) {
    event.preventDefault();

    if (!isAuthenticated || !token) {
      setError(
        "Your session has expired. Please log in again."
      );
      return;
    }

    if (!role.trim()) {
      setError("Please enter a role.");
      return;
    }

    setLoading(true);
    setError(null);
    setAnswer("");
    setEvaluation(null);

    try {
      const result =
        await startMockInterview(
          {
            role: role.trim(),
            difficulty,
            question_count: questionCount,
          },
          token
        );

      setSession(result);

      localStorage.setItem(
        "mock_interview_session_id",
        result.session_id
      );

      setState(
        result.status === "completed"
          ? "completed"
          : "active"
      );
    } catch (err) {
      console.error(
        "Failed to start mock interview:",
        err
      );

      setError(
        err instanceof Error
          ? err.message
          : "Failed to start the interview."
      );
    } finally {
      setLoading(false);
    }
  }


  async function handleSubmitAnswer(
    event: FormEvent
  ) {
    event.preventDefault();

    if (!isAuthenticated || !token) {
      setError(
        "Your session has expired. Please log in again."
      );
      return;
    }

    if (!session?.session_id) {
      setError(
        "No active interview session was found."
      );
      return;
    }

    if (!answer.trim()) {
      setError(
        "Please enter an answer first."
      );
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result =
        await submitMockInterviewAnswer(
          session.session_id,
          answer.trim(),
          token
        );

      setSession(result);
      setAnswer("");

      if (
        result.status === "completed"
      ) {
        localStorage.removeItem(
          "mock_interview_session_id"
        );

        setState("completed");
      }
    } catch (err) {
      console.error(
        "Failed to submit interview answer:",
        err
      );

      setError(
        err instanceof Error
          ? err.message
          : "Failed to submit your answer."
      );
    } finally {
      setLoading(false);
    }
  }


  async function handleEvaluateInterview() {
    if (!isAuthenticated || !token) {
      setError(
        "Your session has expired. Please log in again."
      );
      return;
    }

    if (!session?.session_id) {
      setError(
        "No completed interview session was found."
      );
      return;
    }

    setEvaluating(true);
    setError(null);

    try {
      const result =
        await evaluateMockInterview(
          session.session_id,
          token
        );

      setEvaluation(result);
      setState("results");
    } catch (err) {
      console.error(
        "Failed to evaluate interview:",
        err
      );

      setError(
        err instanceof Error
          ? err.message
          : "Failed to evaluate the interview."
      );
    } finally {
      setEvaluating(false);
    }
  }


  function resetInterview() {
    localStorage.removeItem(
      "mock_interview_session_id"
    );

    setSession(null);
    setEvaluation(null);
    setAnswer("");
    setError(null);
    setEvaluating(false);
    setState("setup");
  }


  if (authLoading || restoring) {
    return (
      <DashboardLayout>
        <div className="flex min-h-[70vh] items-center justify-center">
          <div className="flex items-center gap-3 text-sm text-slate-400">
            <Loader2
              size={18}
              className="animate-spin text-blue-400"
            />

            {authLoading
              ? "Checking your session..."
              : "Checking for an active interview..."}
          </div>
        </div>
      </DashboardLayout>
    );
  }


  if (!isAuthenticated) {
    return (
      <DashboardLayout>
        <div className="flex min-h-[70vh] items-center justify-center">
          <div className="w-full max-w-3xl rounded-3xl border border-slate-800 bg-slate-900/80 p-8 text-center shadow-2xl">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-blue-500/10 text-blue-400">
              <MessageSquareText size={24} />
            </div>

            <h1 className="mt-5 text-2xl font-bold text-white">
              Login required
            </h1>

            <p className="mt-2 text-sm leading-6 text-slate-400">
              Please log in before starting a mock
              interview.
            </p>
          </div>
        </div>
      </DashboardLayout>
    );
  }


  return (
    <DashboardLayout>
      <main className="w-full px-4 py-8 text-white sm:px-6 lg:px-8">
        <div className="mx-auto max-w-6xl">

          {/* =====================================================
              Header
          ====================================================== */}

          <header className="mb-8">
            <div className="flex items-start gap-4">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl border border-blue-500/20 bg-blue-500/10 text-blue-400">
                <MessageSquareText size={22} />
              </div>

              <div>
                <p className="text-xs font-medium uppercase tracking-[0.22em] text-blue-400">
                  AI Interview Preparation
                </p>

                <h1 className="mt-1 text-3xl font-bold tracking-tight sm:text-4xl">
                  Mock Interview
                </h1>

                <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400 sm:text-base">
                  Practice role-specific technical
                  interviews with questions tailored
                  to your resume.
                </p>
              </div>
            </div>
          </header>


          {/* =====================================================
              Error
          ====================================================== */}

          {error && (
            <div className="mb-6 rounded-2xl border border-red-500/20 bg-red-500/5 px-5 py-4 text-sm text-red-300">
              {error}
            </div>
          )}


          {/* =====================================================
              EXISTING SESSION CHOICE
          ====================================================== */}

          {state === "resume-choice" &&
            session && (
              <section className="mx-auto max-w-3xl">
                <div className="overflow-hidden rounded-3xl border border-blue-500/20 bg-slate-900/80 shadow-2xl shadow-black/20">

                  <div className="border-b border-slate-800 px-6 py-7 sm:px-8">
                    <div className="flex items-center gap-3">
                      <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
                        <Clock3 size={21} />
                      </div>

                      <div>
                        <p className="text-xs font-medium uppercase tracking-[0.18em] text-blue-400">
                          Interview in progress
                        </p>

                        <h2 className="mt-1 text-2xl font-bold text-white">
                          Welcome back
                        </h2>
                      </div>
                    </div>
                  </div>

                  <div className="px-6 py-7 sm:px-8">
                    <p className="text-sm leading-7 text-slate-400">
                      You already have an unfinished
                      interview session. Continue where
                      you left off, or start a completely
                      new interview.
                    </p>

                    <div className="mt-6 grid gap-3 sm:grid-cols-3">

                      <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                        <p className="text-xs uppercase tracking-wider text-slate-600">
                          Role
                        </p>

                        <p className="mt-2 text-sm font-semibold text-white">
                          {session.role}
                        </p>
                      </div>

                      <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                        <p className="text-xs uppercase tracking-wider text-slate-600">
                          Progress
                        </p>

                        <p className="mt-2 text-sm font-semibold text-white">
                          Question{" "}
                          {session.question_number}{" "}
                          of{" "}
                          {session.total_questions}
                        </p>
                      </div>

                      <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
                        <p className="text-xs uppercase tracking-wider text-slate-600">
                          Difficulty
                        </p>

                        <p className="mt-2 text-sm font-semibold capitalize text-white">
                          {session.difficulty}
                        </p>
                      </div>

                    </div>

                    <div className="mt-7 flex flex-col gap-3 sm:flex-row">

                      <button
                        type="button"
                        onClick={
                          continueExistingInterview
                        }
                        className="flex flex-1 items-center justify-center gap-2 rounded-2xl bg-blue-600 px-5 py-3.5 text-sm font-semibold text-white transition hover:bg-blue-500"
                      >
                        Continue Interview
                        <ArrowRight size={18} />
                      </button>

                      <button
                        type="button"
                        onClick={
                          startNewInterview
                        }
                        className="flex flex-1 items-center justify-center gap-2 rounded-2xl border border-slate-700 bg-slate-950/70 px-5 py-3.5 text-sm font-semibold text-slate-300 transition hover:border-slate-600 hover:bg-slate-900 hover:text-white"
                      >
                        <RotateCcw size={17} />
                        Start New Interview
                      </button>

                    </div>
                  </div>
                </div>
              </section>
            )}


          {/* =====================================================
              SETUP
          ====================================================== */}

          {state === "setup" && (
            <section className="grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">

              <form
                onSubmit={handleStartInterview}
                className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6 shadow-2xl shadow-black/20 sm:p-8"
              >
                <div className="mb-8">
                  <div className="flex items-center gap-2 text-sm text-blue-400">
                    <Sparkles size={16} />
                    Interview Setup
                  </div>

                  <h2 className="mt-2 text-2xl font-semibold text-white">
                    Configure your practice session
                  </h2>

                  <p className="mt-2 text-sm leading-6 text-slate-400">
                    Choose the target role, difficulty,
                    and number of questions.
                  </p>
                </div>


                {/* Role */}

                <div>
                  <label
                    htmlFor="role"
                    className="mb-2 block text-sm font-medium text-slate-200"
                  >
                    Target role
                  </label>

                  <div className="relative">
                    <BriefcaseBusiness
                      size={18}
                      className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-slate-500"
                    />

                    <input
                      id="role"
                      value={role}
                      onChange={(event) =>
                        setRole(
                          event.target.value
                        )
                      }
                      placeholder="e.g. Backend Engineer"
                      className="w-full rounded-2xl border border-slate-800 bg-slate-950/80 py-3.5 pl-11 pr-4 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/10"
                      disabled={loading}
                    />
                  </div>
                </div>


                {/* Difficulty */}

                <div className="mt-7">
                  <div className="mb-3 flex items-center justify-between">
                    <label className="text-sm font-medium text-slate-200">
                      Difficulty
                    </label>

                    <span className="text-xs text-slate-500">
                      Select one
                    </span>
                  </div>

                  <div className="grid gap-3 sm:grid-cols-3">
                    {DIFFICULTIES.map(
                      (option) => {
                        const selected =
                          difficulty ===
                          option.value;

                        return (
                          <button
                            key={option.value}
                            type="button"
                            onClick={() =>
                              setDifficulty(
                                option.value
                              )
                            }
                            disabled={loading}
                            className={`rounded-2xl border p-4 text-left transition ${
                              selected
                                ? "border-blue-500/50 bg-blue-500/10"
                                : "border-slate-800 bg-slate-950/70 hover:border-slate-700"
                            }`}
                          >
                            <div className="flex items-center justify-between">
                              <span
                                className={`text-sm font-semibold ${
                                  selected
                                    ? "text-blue-300"
                                    : "text-white"
                                }`}
                              >
                                {option.label}
                              </span>

                              <CircleDot
                                size={17}
                                className={
                                  selected
                                    ? "text-blue-400"
                                    : "text-slate-700"
                                }
                              />
                            </div>

                            <p className="mt-1 text-xs text-slate-500">
                              {option.description}
                            </p>
                          </button>
                        );
                      }
                    )}
                  </div>
                </div>


                {/* Question count */}

                <div className="mt-7">
                  <div className="mb-3 flex items-center justify-between">
                    <label className="text-sm font-medium text-slate-200">
                      Questions
                    </label>

                    <span className="text-xs text-slate-500">
                      More questions = longer session
                    </span>
                  </div>

                  <div className="flex flex-wrap gap-3">
                    {QUESTION_OPTIONS.map(
                      (count) => {
                        const selected =
                          questionCount ===
                          count;

                        return (
                          <button
                            key={count}
                            type="button"
                            onClick={() =>
                              setQuestionCount(
                                count
                              )
                            }
                            disabled={loading}
                            className={`min-w-16 rounded-xl border px-4 py-2.5 text-sm font-medium transition ${
                              selected
                                ? "border-blue-500/50 bg-blue-500/10 text-blue-300"
                                : "border-slate-800 bg-slate-950/70 text-slate-400 hover:border-slate-700 hover:text-white"
                            }`}
                          >
                            {count}
                          </button>
                        );
                      }
                    )}
                  </div>
                </div>


                {/* Start */}

                <button
                  type="submit"
                  disabled={loading}
                  className="mt-8 flex w-full items-center justify-center gap-2 rounded-2xl bg-blue-600 px-5 py-3.5 text-sm font-semibold text-white shadow-lg shadow-blue-950/30 transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {loading ? (
                    <>
                      <Loader2
                        size={18}
                        className="animate-spin"
                      />
                      Preparing Interview...
                    </>
                  ) : (
                    <>
                      Start Interview
                      <ArrowRight size={18} />
                    </>
                  )}
                </button>
              </form>


              {/* Preview */}

              <div className="rounded-3xl border border-slate-800 bg-gradient-to-br from-slate-900 to-slate-950 p-6 sm:p-8">
                <div className="flex items-center gap-2 text-sm text-blue-400">
                  <Target size={16} />
                  What to expect
                </div>

                <h3 className="mt-2 text-2xl font-semibold text-white">
                  A focused technical practice session
                </h3>

                <div className="mt-8 space-y-4">

                  {[
                    {
                      icon: Sparkles,
                      title: "Role-aware questions",
                      description:
                        "Questions are generated around your selected role and resume.",
                    },
                    {
                      icon: Clock3,
                      title: "One question at a time",
                      description:
                        "Stay focused without seeing the entire interview at once.",
                    },
                    {
                      icon: CheckCircle2,
                      title: "Progress tracking",
                      description:
                        "Track where you are in the session and complete it cleanly.",
                    },
                  ].map((item) => {
                    const Icon = item.icon;

                    return (
                      <div
                        key={item.title}
                        className="flex gap-4 rounded-2xl border border-slate-800 bg-slate-950/60 p-4"
                      >
                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
                          <Icon size={18} />
                        </div>

                        <div>
                          <h4 className="text-sm font-semibold text-white">
                            {item.title}
                          </h4>

                          <p className="mt-1 text-sm leading-6 text-slate-500">
                            {item.description}
                          </p>
                        </div>
                      </div>
                    );
                  })}

                </div>
              </div>
            </section>
          )}


          {/* =====================================================
              ACTIVE INTERVIEW
          ====================================================== */}

          {state === "active" &&
            session && (
              <section className="mx-auto max-w-5xl">

                <div className="mb-5 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <div className="flex items-center gap-2 text-xs uppercase tracking-[0.18em] text-slate-500">
                      <BriefcaseBusiness
                        size={14}
                      />

                      {session.role}
                    </div>

                    <h2 className="mt-1 text-xl font-semibold text-white">
                      Technical Interview
                    </h2>
                  </div>

                  <div className="flex items-center gap-2 rounded-full border border-slate-800 bg-slate-900/80 px-4 py-2 text-sm text-slate-300">
                    Question{" "}
                    <span className="font-semibold text-white">
                      {session.question_number}
                    </span>

                    <span className="text-slate-600">
                      /
                    </span>

                    {session.total_questions}
                  </div>
                </div>


                <div className="mb-6 h-1.5 overflow-hidden rounded-full bg-slate-900">
                  <div
                    className="h-full rounded-full bg-blue-500 transition-all duration-500"
                    style={{
                      width: `${getProgress(
                        session.question_number,
                        session.total_questions
                      )}%`,
                    }}
                  />
                </div>


                <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-black/20 sm:p-8">
                  <div className="flex flex-col gap-6">

                    <div className="flex flex-wrap items-center gap-2">
                      <span className="rounded-full border border-blue-500/20 bg-blue-500/10 px-3 py-1.5 text-xs font-medium text-blue-300">
                        {session.category ||
                          "Technical"}
                      </span>

                      <span className="rounded-full border border-slate-800 bg-slate-950 px-3 py-1.5 text-xs text-slate-500">
                        {session.difficulty}
                      </span>
                    </div>


                    <div>
                      <p className="text-xs font-medium uppercase tracking-[0.18em] text-slate-500">
                        Interview Question
                      </p>

                      <h2 className="mt-3 text-2xl font-semibold leading-9 text-white sm:text-3xl sm:leading-[1.35]">
                        {session.question}
                      </h2>
                    </div>


                    <form
                      onSubmit={
                        handleSubmitAnswer
                      }
                    >
                      <label
                        htmlFor="answer"
                        className="mb-3 block text-sm font-medium text-slate-200"
                      >
                        Your answer
                      </label>

                      <textarea
                        id="answer"
                        value={answer}
                        onChange={(event) =>
                          setAnswer(
                            event.target.value
                          )
                        }
                        placeholder="Explain your reasoning clearly. Use examples where relevant."
                        className="min-h-[260px] w-full resize-y rounded-2xl border border-slate-800 bg-slate-950/80 p-5 text-sm leading-7 text-white outline-none transition placeholder:text-slate-600 focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/10"
                        disabled={loading}
                      />

                      <div className="mt-4 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                        <p className="text-xs leading-5 text-slate-600">
                          Your answer will be stored as part
                          of this interview session.
                        </p>

                        <button
                          type="submit"
                          disabled={
                            loading ||
                            !answer.trim()
                          }
                          className="flex items-center justify-center gap-2 rounded-2xl bg-blue-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
                        >
                          {loading ? (
                            <>
                              <Loader2
                                size={17}
                                className="animate-spin"
                              />
                              Submitting...
                            </>
                          ) : (
                            <>
                              Submit Answer
                              <ChevronRight
                                size={18}
                              />
                            </>
                          )}
                        </button>
                      </div>
                    </form>
                  </div>
                </div>
              </section>
            )}


          {/* =====================================================
              COMPLETED
          ====================================================== */}

          {state === "completed" && (
            <section className="mx-auto max-w-3xl">
              <div className="overflow-hidden rounded-3xl border border-slate-800 bg-slate-900/80 text-center shadow-2xl shadow-black/20">
                <div className="relative px-6 py-14 sm:px-10">

                  <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full border border-green-500/20 bg-green-500/10 text-green-400">
                    <Trophy size={32} />
                  </div>

                  <p className="mt-6 text-xs font-medium uppercase tracking-[0.2em] text-green-400">
                    Interview Complete
                  </p>

                  <h2 className="mt-2 text-3xl font-bold text-white sm:text-4xl">
                    Nice work.
                  </h2>

                  <p className="mx-auto mt-4 max-w-xl text-sm leading-7 text-slate-400 sm:text-base">
                    You completed the interview. Now let
                    InterviewPilot analyze your answers and
                    give you personalized performance
                    feedback.
                  </p>

                  <div className="mx-auto mt-8 rounded-2xl border border-slate-800 bg-slate-950/70 p-5 text-left">
                    <div className="flex items-start gap-3">
                      <Sparkles
                        size={20}
                        className="mt-0.5 shrink-0 text-blue-400"
                      />

                      <div>
                        <p className="text-sm font-semibold text-white">
                          AI Interview Evaluation
                        </p>

                        <p className="mt-1 text-sm leading-6 text-slate-500">
                          Get scores for technical knowledge,
                          communication, relevance, and
                          problem-solving, along with detailed
                          feedback.
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:justify-center">

                    <button
                      type="button"
                      onClick={
                        handleEvaluateInterview
                      }
                      disabled={evaluating}
                      className="inline-flex items-center justify-center gap-2 rounded-2xl bg-blue-600 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-blue-950/30 transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
                    >
                      {evaluating ? (
                        <>
                          <Loader2
                            size={18}
                            className="animate-spin"
                          />
                          Evaluating Interview...
                        </>
                      ) : (
                        <>
                          <Sparkles size={18} />
                          Evaluate My Interview
                        </>
                      )}
                    </button>

                    <button
                      type="button"
                      onClick={
                        resetInterview
                      }
                      className="inline-flex items-center justify-center gap-2 rounded-2xl border border-slate-700 bg-slate-900 px-6 py-3.5 text-sm font-semibold text-slate-300 transition hover:border-slate-600 hover:bg-slate-800 hover:text-white"
                    >
                      <RotateCcw size={17} />
                      Start New Interview
                    </button>

                  </div>
                </div>
              </div>
            </section>
          )}


          {/* =====================================================
              RESULTS
          ====================================================== */}

          {state === "results" &&
            evaluation && (
              <section className="mx-auto max-w-6xl space-y-6">

                {/* Results Header */}

                <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-black/20 sm:p-8">
                  <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">

                    <div>
                      <p className="text-xs font-medium uppercase tracking-[0.2em] text-blue-400">
                        Interview Evaluation
                      </p>

                      <h2 className="mt-2 text-3xl font-bold text-white sm:text-4xl">
                        Your Interview Results
                      </h2>

                      <p className="mt-3 max-w-2xl text-sm leading-7 text-slate-400 sm:text-base">
                        {evaluation.summary}
                      </p>
                    </div>

                    <div className="flex h-32 w-32 shrink-0 flex-col items-center justify-center rounded-full border-4 border-blue-500/30 bg-blue-500/10">
                      <span className="text-4xl font-bold text-blue-300">
                        {evaluation.overall_score}
                      </span>

                      <span className="mt-1 text-xs uppercase tracking-[0.2em] text-slate-500">
                        Overall
                      </span>
                    </div>

                  </div>
                </div>


                {/* Score Cards */}

                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                  {[
                    {
                      label: "Technical",
                      value:
                        evaluation.technical_score,
                    },
                    {
                      label: "Relevance",
                      value:
                        evaluation.relevance_score,
                    },
                    {
                      label: "Communication",
                      value:
                        evaluation.communication_score,
                    },
                    {
                      label: "Problem Solving",
                      value:
                        evaluation.problem_solving_score,
                    },
                  ].map((metric) => (
                    <div
                      key={metric.label}
                      className="rounded-2xl border border-slate-800 bg-slate-900/70 p-5"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-slate-400">
                          {metric.label}
                        </span>

                        <span className="text-xl font-bold text-white">
                          {metric.value}
                        </span>
                      </div>

                      <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-950">
                        <div
                          className="h-full rounded-full bg-blue-500 transition-all duration-700"
                          style={{
                            width: `${Math.max(
                              0,
                              Math.min(
                                100,
                                metric.value
                              )
                            )}%`,
                          }}
                        />
                      </div>
                    </div>
                  ))}
                </div>


                {/* Strengths / Weaknesses */}

                <div className="grid gap-6 lg:grid-cols-2">

                  <div className="rounded-3xl border border-green-500/20 bg-green-500/5 p-6 sm:p-7">
                    <div className="flex items-center gap-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-green-500/10 text-green-400">
                        <CheckCircle2 size={20} />
                      </div>

                      <h3 className="text-xl font-semibold text-white">
                        Strengths
                      </h3>
                    </div>

                    <div className="mt-5 space-y-3">
                      {evaluation.strengths.length >
                      0 ? (
                        evaluation.strengths.map(
                          (strength, index) => (
                            <div
                              key={`${strength}-${index}`}
                              className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm leading-6 text-slate-300"
                            >
                              {strength}
                            </div>
                          )
                        )
                      ) : (
                        <p className="text-sm text-slate-500">
                          No specific strengths were
                          identified.
                        </p>
                      )}
                    </div>
                  </div>


                  <div className="rounded-3xl border border-red-500/20 bg-red-500/5 p-6 sm:p-7">
                    <div className="flex items-center gap-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-red-500/10 text-red-400">
                        <Target size={20} />
                      </div>

                      <h3 className="text-xl font-semibold text-white">
                        Areas to Improve
                      </h3>
                    </div>

                    <div className="mt-5 space-y-3">
                      {evaluation.weaknesses.length >
                      0 ? (
                        evaluation.weaknesses.map(
                          (weakness, index) => (
                            <div
                              key={`${weakness}-${index}`}
                              className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 text-sm leading-6 text-slate-300"
                            >
                              {weakness}
                            </div>
                          )
                        )
                      ) : (
                        <p className="text-sm text-slate-500">
                          No major weaknesses were
                          identified.
                        </p>
                      )}
                    </div>
                  </div>

                </div>


                {/* Improvement Suggestions */}

                <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6 sm:p-7">

                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
                      <Sparkles size={20} />
                    </div>

                    <div>
                      <h3 className="text-xl font-semibold text-white">
                        How to Improve
                      </h3>

                      <p className="mt-1 text-sm text-slate-500">
                        Actionable suggestions based on
                        your performance.
                      </p>
                    </div>
                  </div>

                  <div className="mt-5 space-y-3">
                    {evaluation.improvement_suggestions.length >
                    0 ? (
                      evaluation.improvement_suggestions.map(
                        (suggestion, index) => (
                          <div
                            key={`${suggestion}-${index}`}
                            className="flex gap-3 rounded-2xl border border-slate-800 bg-slate-950/60 p-4"
                          >
                            <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-blue-500/10 text-xs font-semibold text-blue-400">
                              {index + 1}
                            </span>

                            <p className="text-sm leading-6 text-slate-300">
                              {suggestion}
                            </p>
                          </div>
                        )
                      )
                    ) : (
                      <p className="text-sm text-slate-500">
                        No improvement suggestions are
                        available.
                      </p>
                    )}
                  </div>
                </div>


                {/* Question Feedback */}

                <div className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6 sm:p-7">

                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-purple-500/10 text-purple-400">
                      <MessageSquareText size={20} />
                    </div>

                    <div>
                      <h3 className="text-xl font-semibold text-white">
                        Question-by-Question Feedback
                      </h3>

                      <p className="mt-1 text-sm text-slate-500">
                        See how each response could be
                        improved.
                      </p>
                    </div>
                  </div>

                  <div className="mt-6 space-y-3">
                    {evaluation.question_feedback.length >
                    0 ? (
                      evaluation.question_feedback.map(
                        (feedback, index) => (
                          <div
                            key={`${feedback}-${index}`}
                            className="rounded-2xl border border-slate-800 bg-slate-950/60 p-5"
                          >
                            <div className="flex gap-4">
                              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-slate-800 text-xs font-bold text-slate-300">
                                {index + 1}
                              </div>

                              <p className="text-sm leading-7 text-slate-300">
                                {feedback}
                              </p>
                            </div>
                          </div>
                        )
                      )
                    ) : (
                      <p className="text-sm text-slate-500">
                        No question-level feedback is
                        available.
                      </p>
                    )}
                  </div>
                </div>


                {/* Actions */}

                <div className="flex justify-center pb-8">
                  <button
                    type="button"
                    onClick={
                      resetInterview
                    }
                    className="inline-flex items-center gap-2 rounded-2xl border border-slate-700 bg-slate-900 px-6 py-3.5 text-sm font-semibold text-slate-300 transition hover:border-slate-600 hover:bg-slate-800 hover:text-white"
                  >
                    <RotateCcw size={17} />
                    Start New Interview
                  </button>
                </div>

              </section>
            )}

        </div>
      </main>
    </DashboardLayout>
  );
}