import math

import pytest

from crochet_checker.ai_providers.settings import ConsensusSettings


def test_defaults_are_conservative_and_requires_two_reviewers():
    settings = ConsensusSettings.from_env({})
    assert settings.min_participating_models == 2
    assert settings.min_participation_ratio == 1.0
    assert settings.enable_cross_examination is True
    assert settings.enable_adversarial_review is True
    assert settings.strict_required_participation is True
    assert settings.required_roles == ("stitch_arithmetic", "construction_assembly")
    assert settings.required_participant_target(2) == 2


def test_environment_values_are_bounded_and_nonfinite_values_are_not_trusted():
    settings = ConsensusSettings.from_env(
        {
            "CROCHET_CONSENSUS_MIN_MODELS": "100",
            "CROCHET_CONSENSUS_MIN_PARTICIPATION_RATIO": "nan",
            "CROCHET_CONSENSUS_THRESHOLD": "0.72",
            "CROCHET_CONSENSUS_MAX_CONCURRENCY": "0",
            "CROCHET_CONSENSUS_MAX_REVISIONS": "999",
            "CROCHET_REQUIRED_REVIEW_ROLES": "stitch_arithmetic,construction_assembly",
        }
    )
    assert settings.min_participating_models == 32
    assert settings.min_participation_ratio == 1.0
    assert settings.consensus_threshold == 0.72
    assert settings.max_concurrency == 1
    assert settings.max_revisions == 10
    assert settings.required_participant_target(3) == 32


def test_invalid_direct_values_fail_instead_of_being_silently_accepted():
    with pytest.raises(ValueError, match="between 1 and 32"):
        ConsensusSettings(min_participating_models=0)
    with pytest.raises(ValueError, match="between 0.5 and 1"):
        ConsensusSettings(consensus_threshold=0.4)
    with pytest.raises(ValueError, match="between 0 and 1"):
        ConsensusSettings(min_participation_ratio=math.inf)
    with pytest.raises(ValueError, match="include stitch_arithmetic"):
        ConsensusSettings(required_roles=("custom_role",))
    with pytest.raises(ValueError, match="cannot be disabled"):
        ConsensusSettings(strict_required_participation=False)
