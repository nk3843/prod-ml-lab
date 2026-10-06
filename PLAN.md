# Prod ML Lab — Plan

Productionizing a taxi trip duration model, one layer at a time.

**Golden rule:** every layer ends with a result in results.md and a list of
failure modes checked. Never two half-finished layers. Predict before every run.

**Task:** predict trip duration (minutes) for NYC yellow taxi trips at request
time (pickup time, pickup/dropoff zone, passenger count, distance estimate).
**Data:** NYC TLC public parquet files, a few months. **Metric:** MAE (minutes),
plus p50/p99 latency for serving.

Each layer lists **Failure modes** to design against before building.

## Layer 0: Concepts (~1h)
**Goal:** explain the lifecycle of a deployed model without notes.
**Steps:** Huyen ch. 1 (overview), 7 (deployment), 8 (distribution shifts and
monitoring), 9 (continual learning and testing in production), in that order.
**Done when:** you can draw train → serve → monitor → retrain from memory and
name where each failure below enters.
**Trap:** passive reading. Explain each section aloud first.

## Layer 1: Honest baseline in a notebook
**Goal:** a trustworthy offline number.
**Steps:** download 3-4 months → clean → time-based split (train on early
months, validate on the next, test on the last) → mean/median and linear
baselines → GBM → MAE overall and by slice (hour, borough, distance bucket).
**Done when:** baselines and GBM are in results.md with slice breakdown.
**Failure modes:** random split leaking future into past; dropoff-derived
features (e.g. actual distance, dropoff time) unavailable at request time;
garbage rows (negative or 0-minute trips, 24h trips) distorting MAE;
a good average hiding bad slices.

## Layer 2: Pipeline and shared features
**Goal:** the notebook becomes reproducible code with no train/serve skew.
**Steps:** move to a package; one `features.py` used by training and serving;
config for paths and params; fixed seeds; dataset and model versioned by hash.
**Done when:** `make train` reproduces the Layer 1 number; a test proves
training features equal serving features for the same raw input.
**Failure modes:** skew from duplicated feature code; unseen categories at
serving; nulls and wrong dtypes; nondeterministic training; silent library
version changes.

## Layer 3: Prediction service (local)
**Goal:** a FastAPI service with a validated contract.
**Steps:** pydantic schema, `/predict`, `/health`, model loaded once at
startup, structured logging of every request and prediction; unit and contract
tests; online vs batch comparison; latency benchmark.
**Done when:** p50/p99 latency and throughput are in results.md.
**Failure modes:** malformed or out-of-range input; model file missing or
wrong version at startup; per-request model load; unbounded batch size;
logging that leaks or blows up disk.

## Layer 4: Container, CI, deploy
**Goal:** a live public endpoint.
**Steps:** slim Dockerfile → GitHub Actions (lint, tests, build) → deploy to a
free tier (Render by default: no card needed; note Fly.io and Cloud Run need
billing info) → smoke test against the live URL.
**Done when:** a live URL answers `/predict` and CI is green.
**Failure modes:** works locally but not in the container (paths, arch);
cold starts on free tier (measure and document); image too big; secrets in
the repo; deploy of a broken build (CI gate, health check, rollback).

## Layer 5: Monitoring
**Goal:** know when the model is wrong before users do.
**Steps:** log inputs and predictions; join delayed ground truth later (true
duration arrives after the trip); input drift (PSI/KS), prediction drift,
live MAE; simple dashboard; alert thresholds.
**Done when:** a report shows drift and live MAE between two time windows.
**Failure modes:** monitoring only latency and uptime; labels arrive late so
accuracy lags; alert thresholds that are too noisy or too quiet; drift
metric flags harmless change.

## Layer 6: Break it on purpose
**Goal:** see each failure appear in the monitoring you built.
**Steps:** (1) replay later months and watch drift; (2) a sudden upstream
schema or unit change (miles to km); (3) load spike; (4) an invalid-input
flood; (5) cold start.
**Done when:** one line per failure: how it showed up, how long to detect,
and the fix.
**Trap:** fixing before you've recorded how it showed up.

## Layer 7: Continual learning and safe rollout
**Goal:** retrain and ship a new model without taking the service down.
**Steps:** retrain trigger (drift or schedule); model registry/versioning;
shadow deployment, then canary; compare candidate vs current on live traffic.
**Done when:** a candidate model ran in shadow and a promotion decision is
recorded with numbers.
**Failure modes:** retraining on bad or poisoned data; new model worse on a
slice; no rollback path; feedback loops.

## Layer 8: Write-up and oral check (~1.5h)
**Done when:** README has an architecture diagram, one section per layer
(problem, what I built, measured result, what broke), the results table, and
the live URL; one-page cheat sheet; 5 oral questions answered.

## Progress
- [ ] Layer 0 - [ ] Layer 1 - [ ] Layer 2 - [ ] Layer 3
- [ ] Layer 4 - [ ] Layer 5 - [ ] Layer 6 - [ ] Layer 7 - [ ] Layer 8
- [ ] Recall check in 2-3 days
