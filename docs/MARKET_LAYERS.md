# The Market's Real Layers — by Direction of Capital Flow

The rigorous role taxonomy behind MicroWorld's agent universe. The market
is layered **by function along the direction money flows** — not by
company, and not by the four-level game abstraction the mathematics solves
(that abstraction is a *projection* of this map; see
[the mapping](#how-microworld-consumes-this-map) at the end).

*中文原文在文末附錄。US market focus; the taxonomy itself is general.*

---

## Main chain — money flowing downstream, Layer 0 → Layer 6

### Layer 0 · The original surplus sector (where money begins)
- Retail / individual investors
- High-net-worth (HNWI) and ultra-high-net-worth (UHNWI) individuals
- Non-financial corporate retained earnings; corporate treasury
- Government fiscal surpluses; FX reserves
- Overseas sector (cross-border savings inflows)

### Layer 1 · Institutionalized asset owners (liability-side constraints)
- **Retirement**: public pensions (GPIF, CalPERS), corporate DB/DC plans, sovereign pension reserve funds
- **Insurance**: life, property & casualty, reinsurance
- **Other long-horizon pools**: sovereign wealth funds (GIC, Temasek, Norway GPFG), university endowments, charitable foundations, single/multi-family offices (SFO/MFO), central-bank reserve management, bank treasury investment books

### Layer 2 · Allocation & conduit (decides who manages the money; places no orders)
- **Gatekeepers**: funds-of-funds, manager-of-managers, investment consultants (Mercer, Cambridge Associates), OCIO
- **Wealth channels**: private banks, wealth management, independent advisors (RIA/IFA), robo-advisors, bank distribution, broker wealth management, third-party fund platforms, trust companies
- **Indirect-finance conduit**: the commercial-bank deposit→loan system

### Layer 3 · Asset managers (buy side — turns allocation into positions; the alpha-competition layer)
- **Traditional long-only**: mutual funds, index funds, ETF issuers, SMAs, money-market funds
- **Hedge funds**: equity long/short, quant / stat-arb, CTA / managed futures, global macro, event-driven / merger-arb, credit / distressed, relative-value / fixed-income arb, convertible arb, multi-strategy, tail-risk
- **Private markets**: buyout, growth equity, VC, private credit / direct lending, mezzanine, secondaries, real-estate PE, infrastructure, natural resources
- **Other**: REIT managers, insurance asset management, bank AM subsidiaries, commodity funds, crypto funds, self-directed retail (dual-listed at Layer 0)

### Layer 4 · Sell side & trading intermediaries (fees from access, leverage, spread)
- **Investment banking**: ECM, DCM, M&A advisory, sales & trading, sell-side research, structured products / derivatives desks, sponsors
- **Brokerage & financing**: retail brokers, institutional brokers, FCMs, introducing brokers, prime brokers, securities-lending agents
- **Dealers**: OTC / swap dealers, repo desks, FX dealers, inter-dealer brokers (TP ICAP), commodity traders (Glencore)

### Layer 5 · Market infrastructure (where money and securities actually change hands)
- **Venues**: securities exchanges, futures/options exchanges, ATS/ECN/MTF, dark pools, single-dealer platforms, OTC electronic platforms (Tradeweb, MarketAxess), crypto exchanges
- **Clearing & settlement**: CCPs (LCH, OCC, NSCC), CSDs (DTC, Euroclear, Clearstream), transfer agents
- **Custody & administration**: custodians (BNY Mellon, State Street), fund administrators, TA/registrars
- **Payment networks**: Fedwire/CHIPS, SWIFT (messaging), CLS (FX PvP settlement)

### Layer 6 · Capital demanders (issuers — the final users of money; the primary-market gate)
- **Corporate**: IPO / follow-on, corporate bonds, convertibles, commercial paper, syndicated-loan borrowers
- **Financial-institution funding**: bank debt / AT1, insurance subordinated debt
- **Public sector**: Treasuries, municipal bonds, agencies, supranationals (World Bank, ADB)
- **Structured & other**: securitization SPVs (MBS, ABS, CLO), covered-bond issuers, SPACs, household borrowing (mortgages/consumer credit — securitized back into the market)

## Parallel layer — proprietary-capital traders (outside the client-money chain; interfaces at Layers 4–5)
- Market-making prop firms: Jane Street, Optiver, SIG, IMC, DRW
- High-frequency trading: Virtu, Jump, XTX
- Large market makers: Citadel Securities
- Bank prop desks (constrained post-Volcker)
- Active corporate-treasury operations

## Outer ring 1 — information & pricing auxiliaries (touch no money; steer where it flows)
- Rating agencies (Moody's, S&P, Fitch)
- Index providers (MSCI, S&P DJI, FTSE Russell)
- Market-data vendors (Bloomberg, LSEG/Refinitiv, FactSet); alternative-data vendors
- Independent research; expert networks (GLG)
- Proxy advisors (ISS, Glass Lewis)
- Auditors, law firms, valuation agents
- Financial media; investor relations
- OMS/EMS trading-technology vendors

## Outer ring 2 — rules & last-resort support (spans every layer)
- Central banks (monetary policy, lender of last resort, direct buyer under QE)
- Securities regulators (SEC, SFC, CSRC); futures regulators (CFTC)
- Bank regulators (Fed, OCC, HKMA, Basel Committee)
- Treasuries / finance ministries (issuance + crisis support)
- Deposit insurance (FDIC); investor protection (SIPC)
- Self-regulatory organizations (FINRA)
- International coordination (IMF, BIS, FSB, IOSCO)

## The flow, summarized

> Savings (L0) → institutionalization (L1) → allocation (L2) → positions
> (L3) → access (L4) → settlement (L5) → issuers (L6) → the real economy;
> returns (dividends, interest, principal, buybacks) flow back along the
> same path. The parallel layer earns liquidity money between L4–L5 only;
> the two outer rings never touch the money but set the flow and the rules
> of every segment.

## Usage notes

1. Layers are **functional, not corporate** — JPMorgan appears simultaneously at Layers 2/3/4/5.
2. Some roles are **multi-layer by nature**: retail (L0 + L3), central banks (L1 + outer ring 2), households (L0 savers + L6 borrowers — securitization closes the loop).
3. The outer rings are **"shadow allocators who never touch the money"**: index inclusion and rating changes directly move flows.
4. Crypto runs a parallel copy: stablecoin issuers ≈ issuers, DeFi protocols ≈ infrastructure, validators ≈ settlement.

---

## How MicroWorld consumes this map

| This map | In the model |
|---|---|
| Layers 0–6 (main chain) | The **agent universe** — each layer a family of agent classes with its own objectives, constraints, and information sets ([`agents/`](../agents/)); the current 6+5 class taxonomy is the Phase-1 subset, to be extended layer-by-layer |
| Parallel layer (prop/HFT) | Liquidity-provision agents coupled to the price field (the $w_5$ inventory/gap coupling in the MVP figure) |
| **Outer ring 2** (regulators) | **The constraint modules** — the per-type weight sharing NNGS imposes as architecture; regulation *is* the shared projection layer |
| **Outer ring 1** (index/rating/data) | **The information operators** — filtration structure ([`state/information.py`](../state/information.py)) and flow-steering event operators (index inclusion = a Mode-I operator on μ) |
| The four game levels L0–L3 of the mathematics | The **tractable projection** of this map that Phase 1 solves (hierarchical MFG, Theorem 7.4): game-L0 ≈ aggregate cross-market flow over the whole chain; game-L1 ≈ strategic classes drawn from Layers 1–4 + parallel; game-L2 ≈ individual institutions; game-L3 ≈ desks. **Phase 2 (NNGS) drops the projection and ingests this full layered graph directly.** |

---

<details>
<summary><b>附錄 · 中文原文（完整版）</b></summary>

# 市場角色完整分層（按資金流動方向）

## 主鏈：資金順流方向 第0層 → 第6層

### 第0層 原始盈餘部門（錢最初的來源）
散戶/個人投資者；高淨值個人（HNWI）、超高淨值（UHNWI）；非金融企業留存盈餘、企業財資部門；政府財政盈餘、外匯儲備；海外部門資金（跨境儲蓄流入）

### 第1層 機構化出資人（asset owners，有負債端約束）
退休養老：公共養老金（GPIF、CalPERS）、企業年金（DB/DC）、主權養老儲備基金；保險：壽險、財險、再保險；其他長期資本池：主權財富基金（GIC、Temasek、挪威GPFG）、大學捐贈基金、慈善基金會、單一/聯合家族辦公室（SFO/MFO）、央行儲備管理、銀行財資自有投資

### 第2層 配置與導管層（決定錢給誰管，不直接下單）
守門人：FoF、MOM、投資顧問（Mercer、Cambridge Associates）、OCIO；財富渠道：私人銀行、財富管理、獨立顧問（RIA/IFA）、智能投顧、銀行代銷、券商財富管理、第三方基金平台、信託公司；間接融資導管：商業銀行存貸體系

### 第3層 資產管理人（買方，把配置變成持倉，alpha 競爭層）
傳統多頭：共同基金、指數基金、ETF發行商、SMA/專戶、貨幣市場基金；對沖基金：股票多空、量化/統計套利、CTA、全球宏觀、事件驅動/併購套利、信用/不良資產、相對價值/固收套利、可轉債套利、多策略、尾部風險；私募市場：併購基金、成長股權、VC、私募信貸、夾層資本、S基金、地產私募、基建基金、自然資源基金；其他：REITs管理人、保險資管、銀行理財/資管子公司、商品基金、加密資產基金、散戶自主交易（兼第0層）

### 第4層 賣方與交易中介（靠通道/槓桿/價差收費）
投資銀行：ECM、DCM、M&A、銷售交易、賣方研究、結構化產品/衍生品部門、保薦人；經紀與融資：零售券商、機構經紀、期貨經紀（FCM）、介紹經紀、Prime broker、證券借貸代理；交易商：OTC/衍生品交易商、回購交易商、外匯交易商、貨幣經紀（TP ICAP）、大宗商品貿易商（Glencore）

### 第5層 市場基礎設施（錢與證券實際換手交割處）
交易場所：證券/期貨/期權交易所、ATS/ECN/MTF、暗池、單一交易商平台、OTC電子平台（Tradeweb、MarketAxess）、加密交易所；清算交收：CCP（LCH、OCC、NSCC）、CSD（DTC、Euroclear、Clearstream）、過戶代理；保管與行政：託管行（BNY Mellon、State Street）、基金行政、申贖登記；支付網絡：Fedwire/CHIPS、SWIFT、CLS

### 第6層 資金需求方（發行人，錢的最終使用者，一級市場入口）
企業融資：IPO/增發、公司債、可轉債、商業票據、銀團貸款借款人；金融機構融資：銀行債/AT1、保險次級債；公共部門：國債、地方政府債、機構債、超國家機構；結構化與其他：證券化SPV（MBS、ABS、CLO）、covered bond、SPAC、家庭借款端（證券化後回流市場）

## 平行層：自有資金交易者（不在客戶資金鏈內，對接第4-5層）
做市型自營：Jane Street、Optiver、SIG、IMC、DRW；高頻交易：Virtu、Jump、XTX；大型做市商：Citadel Securities；銀行自營盤（Volcker rule 後受限）；企業財資主動操作

## 外圈1：資訊與定價輔助（不碰資金，但決定資金往哪流）
評級機構（Moody's、S&P、Fitch）；指數公司（MSCI、S&P DJI、FTSE Russell）；行情與數據商（Bloomberg、LSEG、FactSet）、另類數據商；獨立研究、專家網絡（GLG）；代理投票顧問（ISS、Glass Lewis）；審計師、律師事務所、估值機構；財經媒體、投資者關係；OMS/EMS 交易技術商

## 外圈2：規則與最後支持（貫穿所有層次）
央行（貨幣政策、最後貸款人、QE時直接買方）；證券監管（SEC、SFC、中國證監會）、期貨監管（CFTC）；銀行監管（Fed、OCC、HKMA、巴塞爾委員會）；財政部；存款保險（FDIC）、投資者保護（SIPC）；自律組織（FINRA）；國際協調（IMF、BIS、FSB、IOSCO）

## 資金流總結
儲蓄（第0層）→ 機構化（第1層）→ 配置（第2層）→ 持倉（第3層）→ 通道（第4層）→ 交割（第5層）→ 發行人（第6層）→ 實體經濟；報酬沿原路回流。平行層自營資金只在第4-5層之間賺流動性的錢；兩個外圈不經手資金，但決定每一段的流量與規則。

## 使用注意
1. 層次按功能劃分，不按公司劃分——JPMorgan 同時出現在第2/3/4/5層。
2. 部分角色身兼多層：散戶（第0+第3層）、央行（第1層+外圈2）、家庭（第0層出錢+第6層借錢，經證券化形成閉環）。
3. 外圈是「不碰錢的影子配置者」：指數納入與評級直接決定資金進出。
4. 加密平行體系：穩定幣發行商≈發行人、DeFi協議≈基礎設施、驗證者≈結算層。

</details>
