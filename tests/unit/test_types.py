from fnt.types import F2DOT14, fixed
import pytest

F2DOT14_vals = (
    (b"\x7F\xFF", 1.999939),
    (b"\x70\x00", 1.75),
    (b"\x00\x01", 0.00006103515625),
    (b"\x00\x00", 0.0),
    (b"\xFF\xFF", -0.00006103515625),
    (b"\x80\x00", -2.0),
)


@pytest.mark.parametrize("b, v", F2DOT14_vals)
def test_F2DOT14(b: bytes, v: float):
    assert F2DOT14(b) == pytest.approx(v)


fixed_vals = (
    ((0).to_bytes(length=4, signed=True), 0.0),
    ((72090).to_bytes(length=4, signed=True), 1.1),
    ((-65536).to_bytes(length=4, signed=True), -1.0),
    ((-131072).to_bytes(length=4, signed=True), -2.0),
    ((13122354).to_bytes(length=4, signed=True), 200.231234),
    ((139802255).to_bytes(length=4, signed=True), 2133.21312),
)


@pytest.mark.parametrize("b, v", fixed_vals)
def test_fixed(b, v):
    assert fixed(b) == pytest.approx(v, rel=1.1e-4)
