# BLOOM: lattice one-out-of-many proofs (FIT5163 group project)

This is our group's repo for the FIT5163 programming assignment (Monash, Semester 2 2026). We were assigned the paper

> **BLOOM: Bimodal Lattice One-Out-of-Many Proofs and Applications**
> Vadim Lyubashevsky (IBM Research Europe) and Ngoc Khanh Nguyen (EPFL)

and the job is to implement it (or a big enough core chunk of it), test it properly, and then compare what we get against what the paper claims.

The repo is still early. Most of what's below is the plan, and we'll fill in the setup and run sections once there's actual code to run.

## What the paper is about (short version)

A one-out-of-many proof lets you prove you know a secret for *one* entry in a public list without revealing which entry. In lattice terms, you have a list of public keys `t_1 ... t_N` and you prove you know a short vector `s` with `A·s = t_i mod p` for some `i`, without leaking `i` or `s`.

If you put everyone's public key into the list and use the message as input to Fiat-Shamir, you get a **ring signature**. That's the main application the paper goes after (there's also a Falcon-based group signature in Appendix E).

The ideas we need to get our heads around, roughly in the order the paper uses them:

- **Writing the unit vector as a tensor product.** The index `i` becomes a one-hot vector `v` of length N. Committing to that directly would blow up the proof size, so they split `v` into a tensor product of smaller unit vectors (`v = v_1 ⊗ v_2 ⊗ ...`). Then they prove the relation recursively, so the proof stays logarithmic in N.
- **ABDLOP commitments and the LNP22 framework** are used to prove the base case. ABDLOP combines Ajtai and BDLOP commitments, and LNP22 is the proof system from Lyubashevsky, Nguyen and Plançon (Crypto 2022).
- **Bimodal Gaussian rejection sampling.** The paper shows the cheaper bimodal version (from BLISS / DDLL13) can be used throughout the protocol. In the one-out-of-many case this costs nothing extra and makes the proofs smaller.
- **Exact norm proofs.** Earlier schemes only proved a relaxed statement. Proving the exact norm lets them use a much smaller modulus, which is why the public keys come out tiny (around 128 bytes per user).

### Numbers from the paper we want to check

The ring signature parameters (Fig. 10) use `(p, n, m, d, δ) = (65437, 1, 12, 64, 8)`:

| Ring size N | k | Claimed signature size |
|---|---|---|
| 2^6  | 0 | 13.1 KB |
| 2^12 | 2 | 14.1 KB |
| 2^18 | 4 | 15.1 KB |
| 2^24 | 6 | 16.2 KB |

Fig. 1 also claims a 7x to 15x reduction in user public key size compared with earlier lattice ring signatures. Reproducing (or failing to reproduce) the signature sizes above is going to be a big part of our evaluation.

## Scope

The full paper covers ring signatures, group signatures and integer-relation proofs, which is a lot for one semester. Our current plan:

**Planned:**
- Polynomial ring arithmetic over `R_q = Z_q[X]/(X^d + 1)`, plus the NTT where it's worth the effort
- ABDLOP commitment
- Bimodal Gaussian rejection sampling
- The base-case proof (knowledge of a unit vector `v` and a short `s` with `T·v = A·s`)
- The recursive one-out-of-many proof
- A ring signature built on top of that (KeyGen / Sign / Verify) using Fiat-Shamir
- Benchmarks: proof size, sign and verify times as N grows, rejection rates

**Probably out of scope (we'll explain why in the report):**
- The Falcon-based group signature (Appendix E). It needs trapdoor sampling and verifiable encryption, which is a whole other project.
- Integer addition and multiplication proofs (Appendix D)
- Constant-time or side-channel hardened code. This is a research prototype.

This list will change as we go. If we cut something or simplify it, it goes in the "Deviations from the paper" section below.

## Contributing

Branch naming, commit messages and the full pull / push / PR workflow are in [CONTRIBUTING.md](CONTRIBUTING.md). Please read it before your first push.

## Repo layout

Planned. It will get updated as files actually appear.

```
.
├── src/          # implementation
├── tests/        # unit + correctness tests
├── bench/        # benchmark scripts and raw results
├── docs/         # notes, meeting minutes, diagrams
└── README.md
```

## Setup

TODO: we haven't finalised the language or the dependencies yet. Once we do, this section will list:

- language / compiler version
- required libraries (with versions)
- OS and hardware we tested on
- install commands

## Running it

TODO: commands for the demo, the test suite and the benchmarks, plus what the output should look like.

## Reproducing the paper's results

TODO: the exact commands to regenerate our signature-size and timing tables, and where the raw output gets saved.

## Deviations from the paper

We'll keep this updated. Anything the paper leaves out where we had to make our own call (parameter choices, how a hash is instantiated, sampling details, etc.) goes here with a short reason.

- *(none yet)*

## Third-party code, libraries and AI use

The assignment requires us to be upfront about anything we didn't write ourselves, so this section lists:

- external libraries and what we use them for
- any code adapted from elsewhere (with a link and licence)
- where AI tools were used and what we changed afterwards

- *(nothing yet)*

## Team

| Name | Student ID | Email |
|---|---|---|
| Tushar Jain | 35896493 | tjai0005@student.monash.edu |
| Shanshan Li | 36404179 | slii0373@student.monash.edu |
| Shaopei Fu | 36858579 | sfuu0033@student.monash.edu |
| Mitchell Padula | 33114579 | mpad0004@student.monash.edu |

Who's working on what is tracked through issues and commit history rather than written here. Everyone is expected to understand the whole codebase anyway, since the Q&A can ask any of us about any part of it.

## Key dates

- **Presentation + live demo:** Week 14 (Mon/Tue)
- **Report and code due:** Friday 6 Nov 2026, 23:55

## Reference

V. Lyubashevsky and N. K. Nguyen, *BLOOM: Bimodal Lattice One-Out-of-Many Proofs and Applications*.
