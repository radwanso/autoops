from autoops.core.event_intelligence import analyze_events
from autoops.core.profile_manager import adapt_profile


from autoops.actions.notifier import send_telegram

from autoops.core.system_metrics import collect_system_metrics
from autoops.core.monitor import is_service_running

from autoops.core.behavior import evaluate_behavior
from autoops.core.classifier import classify_incident
from autoops.core.patterns import detect_patterns

from autoops.core.reputation_engine import calculate_reputation
from autoops.core.experience_engine import evaluate_experience
from autoops.core.predictor import predict_failure

from autoops.core.risk_engine import calculate_risk
from autoops.core.mode_engine import calculate_mode

from autoops.core.strategy_engine import choose_strategy
from autoops.core.decision import decide

from autoops.core.policy import evaluate_policy
from autoops.core.intent_engine import classify_intent

from autoops.core.recovery_policy import build_recovery_policy
from autoops.core.recovery_feedback import analyze_recovery_result
from autoops.core.prevention_engine import build_preventive_actions

from autoops.core.response_engine import build_response_plan
from autoops.core.cognitive_engine import build_cognitive_state

from autoops.core.learning import learn_from_behavior
from autoops.core.memory_engine import update_memory

from autoops.core.system_awareness import calculate_system_state


class Brain:

    def push_state_update(self, state):
        try:
            from autoops.web.ws import broadcast_state
            broadcast_state(state)
        except Exception as e:
            print("[WS UPDATE ERROR]", e)



    def send_telegram(self, message):
        return send_telegram(message)

    # =========================
    # SYSTEM
    # =========================
    def adapt_profile(self, payload):
        profile = payload.get("profile", {})
        events = payload.get("events", {})
        risk = payload.get("risk", {})

        return adapt_profile(
            profile,
            events,
            risk
        )

    def analyze_events(self, history):
        return analyze_events(history)

    def collect_system_metrics(self):
        return collect_system_metrics()

    def is_service_running(self, name):
        return is_service_running(name)

    # =========================
    # BEHAVIOR
    # =========================
    def evaluate_behavior(self, state):
        return evaluate_behavior(state)

    def classify_incident(self, state):
        return classify_incident(state)

    def detect_patterns(self, history):
        return detect_patterns(history)

    # =========================
    # INTELLIGENCE
    # =========================
    def calculate_reputation(self, memory):
        return calculate_reputation(memory)

    def evaluate_experience(self, memory):
        return evaluate_experience(memory)

    def predict_failure(self, events, reputation):
        return predict_failure(events, reputation)

    def calculate_risk(self, state):
        return calculate_risk(state)

    def calculate_mode(self, state):
        return calculate_mode(state)

    # =========================
    # DECISION LAYER
    # =========================
    def choose_strategy(self, state):
        return choose_strategy(state)

    def decide(self, state):
        return decide(state)

    def evaluate_policy(self, state):
        return evaluate_policy(state)

    def classify_intent(self, state):
        return classify_intent(state)

    # =========================
    # RECOVERY LAYER
    # =========================
    def build_recovery_policy(self, state):
        return build_recovery_policy(state)

    def analyze_recovery_result(self, state, result):
        return analyze_recovery_result(state, result)

    def build_preventive_actions(self, state):
        return build_preventive_actions(state)

    def build_response_plan(self, state):
        return build_response_plan(state)

    def build_cognitive_state(self, state):
        return build_cognitive_state(state)

    # =========================
    # MEMORY / LEARNING
    # =========================
    def learn_from_behavior(self, profile, history):
        return learn_from_behavior(profile, history)

    def update_memory(self, memory, state):
        return update_memory(memory, state)

    # =========================
    # SYSTEM STATE
    # =========================
    def calculate_system_state(self, state):
        return calculate_system_state(state)

print("BRAIN VERSION 2026")

# SINGLETON INSTANCE
brain = Brain()
