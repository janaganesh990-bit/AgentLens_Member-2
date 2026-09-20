# AgentLens_Member-2
AgentLens: Reliability Intelligence Module 🔍Welcome to the Reliability Intelligence module of AgentLens. This repository contains the code for Member 2's deliverables in our 60-hour hackathon.Our mission is to turn raw agent execution into trustworthy, deterministic reliability evidence. This module sits between the raw AWS telemetry emitted by the agent (Member 1) and the Reliability Lab's chaos/replay engine (Member 3), supplying structured data and AI-driven insights to the platform UI (Member 4).🎯 Scope BoundaryWhat this module DOES:Trace Normalization: Ingests raw AgentCore/OpenTelemetry/CloudWatch payloads and converts them into a stable, unified Run schema.Deterministic Failure Detectors: Pure-function detectors for tool loops, timeouts/retries, wrong-tool selection, and token/cost anomalies.Incident Engine: Converts detector evidence into structured Incident records linked to specific runs.Amazon Bedrock RCA: Generates probable root causes, impacts, and recommended fixes based strictly on supplied deterministic evidence (no invented telemetry).(Conditional) Lightweight Grounding Detector & Change-to-Test Intelligence.What this module DOES NOT DO:Build the support agent or tools (Member 1).Execute chaos injection, replays, or regression testing (Member 3).Implement the frontend UI, AWS API Gateway, or primary DynamoDB architecture (Member 4).Use LLMs as the primary detector for deterministic failures.🏗️ Core ComponentsRun Normalizer: Shields downstream logic from raw provider payload differences.Loop Detector: Flags an incident if the same tool is repeated $\ge 4$ times.Timeout/Retry Detector: Flags repeated timeouts or retries beyond configured boundaries.Wrong-Tool Detector: Compares expected intent against the selected tool/action class.Token Anomaly Detector: Compares current tokens/tool calls/latency against baseline thresholds.Incident Engine: Packages evidence into a standardized incident object.Bedrock RCA Orchestrator: Validates structured JSON root cause output from Bedrock based on the provided incident payload.📜 Integration ContractsAll modules must integrate through stable IDs and payloads. Below are the core schemas exposed by this module.1. The Run Schema (Output from Normalizer)Consumed by detectors, replay (Member 3), UI, and evaluation.{
  "run_id": "run_20260918_001",
  "agent_version": "v1.0.3",
  "prompt_version": "support-v4",
  "request": "Where is order #8271?",
  "events": [
    {
      "seq": 1,
      "type": "agent_decision",
      "timestamp_ms": 0,
      "tool": "get_order",
      "arguments": {"order_id": "8271"}
    }
  ],
  "tool_calls": 7,
  "tokens": 7100,
  "latency_ms": 12400,
  "errors": ["TIMEOUT"],
  "outcome": "FAILED",
  "detected_failures": ["RETRY_LOOP"]
}
2. The DetectorResult SchemaStable pure-function output used by the incident engine and UI.{
  "failure_type": "RETRY_LOOP",
  "severity": "HIGH",
  "confidence": 1.0,
  "evidence": [
    {"seq": 2, "tool": "get_order", "status": "timeout"},
    {"seq": 3, "tool": "get_order", "status": "timeout"}
  ],
  "metrics": {
    "tool_calls": 7,
    "timeouts": 6,
    "tokens": 7100,
    "latency_ms": 12400
  }
}
3. RCA Output (Amazon Bedrock)Result reasoned only from supplied incident evidence.{
  "primary_failure": "Unbounded retry behavior",
  "probable_root_cause": "No retry limit or fallback path",
  "evidence": ["repeated get_order calls", "repeated timeout responses"],
  "impact": ["excessive tool calls", "increased latency"],
  "recommended_action": "limit retries to 2; introduce a fallback response",
  "confidence": 0.95
}
🤝 Handoffs & DependenciesTo Member 1 (Agent): I require exact telemetry attribute contracts (event/span fields) to feed the normalizer.To Member 3 (Reliability Lab): I provide the normalized Run object, pure-function detector logic for your evaluator, and expected failure outputs.To Member 4 (Platform/UI): I provide the API surface payloads for /runs/{run_id}, /incidents, and /incidents/{id}/rca.Integration Rule: I will provide local/mock JSON fixtures for all outputs by Hour 20 so you can build your modules without waiting for my AWS integrations to finalize.🧪 Testing ChecklistWhen testing this module locally, ensure the following fixtures pass:[x] Loop Detector: A fixture with the same tool called 4+ times yields TOOL LOOP/HIGH. A negative fixture yields no incident.[x] Timeout/Retry: Controlled timeouts yield RETRY FAILURE with correct timeout/latency counts.[x] Wrong-Tool: Intent READ vs selected action DELETE yields WRONG TOOL/HIGH.[x] RCA Generator: Structured timeout incident correctly outputs a JSON suggesting bounded retries/fallback without hallucinating telemetry data.[x] Replay Parity: Normalizer handles both original traces and Replay traces (from Member 3) identically.
