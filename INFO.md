# Magnet Simulation - Technical Information

## Simulation Principle

### Magpylib의 자기장 계산 원리

Magpylib은 영구자석의 자기장을 **해석적(analytical)** 방법으로 계산합니다. 수치적 방법(FEM 등)과 달리 정확한 수학적 해를 사용합니다.

#### 1. 등가 전류 모델 (Equivalent Current Model)

영구자석은 **등가 표면 전류**로 모델링됩니다:
- 균일하게 자화된 물체는 표면에 흐르는 전류로 대체 가능
- 표면 전류 밀도: **K = M × n̂** (M: 자화, n̂: 표면 법선)

원통형 자석의 경우:
- 측면에 원형으로 흐르는 표면 전류
- 솔레노이드와 동일한 자기장 분포

#### 2. 비오-사바르 법칙 (Biot-Savart Law)

기본 원리는 비오-사바르 법칙에서 출발:

```
dB = (μ₀/4π) × (I dl × r̂) / r²
```

여기서:
- μ₀: 진공의 투자율
- I: 전류
- dl: 전류 요소
- r: 관측점까지의 거리

#### 3. 원통 자석의 해석적 해 (Analytical Solution)

Magpylib은 원통 자석에 대해 **타원 적분(Elliptic Integrals)**을 사용한 정확한 해석적 해를 사용합니다:

축 방향 자기장 (Bz):
```
Bz = (μ₀M/4π) × [적분 표현식 with K(k), E(k)]
```

여기서 K(k)와 E(k)는 제1종, 제2종 완전 타원 적분입니다.

이 방법의 장점:
- FEM보다 빠른 계산 속도
- 메시 의존성 없음
- 수학적으로 정확한 해

#### 4. 중첩 원리 (Superposition Principle)

복잡한 형상은 기본 자석들의 중첩으로 계산:
```
B_total = Σ B_i
```

### 자석 내부 vs 외부 자기장

**외부 (r > R)**:
- 자기 쌍극자 근사 (먼 거리)
- 정확한 타원 적분 해 (근거리)

**내부 (r < R)**:
- B = μ₀(H + M) = μ₀H + Br
- 반자기장(Demagnetizing field) 고려

### Key Equations
- **Magnetization**: M = Br / μ₀ [A/m]
- **Magnetic permeability of vacuum**: μ₀ = 4π × 10⁻⁷ [H/m]
- **Field units**: 1 T = 10,000 G (Gauss)
- **Surface current density**: K = M × n̂ [A/m]

---

## Magnet Parameters (YXG-32H Sm₂Co₁₇)

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| **Material** | - | Sm₂Co₁₇ (Samarium Cobalt) | - |
| **Grade** | - | YXG-32H | - |
| **Remanence** | Br | 1.10 – 1.13 (avg: 1.115) | T |
| **Coercivity Force** | Hcb | 812 – 860 (avg: 836) | kA/m |
| **Intrinsic Coercivity** | Hcj | ≥ 1990 | kA/m |
| **Max Energy Product** | (BH)max | 230 – 255 (avg: 242.5) | kJ/m³ |
| **Max Working Temp** | - | 350 | °C |
| **Calculated Magnetization** | M | ~8.87 × 10⁵ | A/m |

---

## Magnet Geometry

| Dimension | Value | Unit |
|-----------|-------|------|
| **Diameter (D)** | 30 | mm |
| **Height (H)** | 35 | mm |
| **Volume** | ~24,740 | mm³ |
| **Magnetization Direction** | +z axis | - |

---

## Visualization Details

### 2D Simulation (magnet_sim_2d.py)
- **Grid**: 300 × 300 points, -60 to +60 mm
- **Colormap**: coolwarm
- **Field lines**: Streamplot with density 1.5
- **Contours**: 500 G (cyan), 1000 G (lime), 2000 G (yellow)

### 3D Simulation (magnet_sim_3d.py)
- **Grid**: 61 × 61 × 61 points, -60 to +60 mm
- **Spacing**: 2 mm
- **Streamlines**: 15 radial seed points per pole
- **Slice plane**: x-z plane (y=0)
- **Isosurface**: 2000 G (0.2 T)

---

## Expected Field Values

| Position (z) | |B| (Gauss) | |B| (Tesla) |
|--------------|-------------|------------|
| Center (0 mm) | ~5,575 | ~0.558 |
| Surface (17.5 mm) | ~3,500 | ~0.350 |
| 1H away (35 mm) | ~1,200 | ~0.120 |
| 2H away (70 mm) | ~400 | ~0.040 |

*Note: Actual values may vary based on calculation resolution*

---

## Libraries Used

- **magpylib**: Analytical magnetic field calculations
- **numpy**: Numerical computations
- **matplotlib**: 2D plotting and 3D matplotlib backend
- **pyvista**: 3D visualization with interactive features

---

## References

1. Magpylib documentation: https://magpylib.readthedocs.io/
2. Sm₂Co₁₇ magnet datasheet: YXG-32H grade specifications
