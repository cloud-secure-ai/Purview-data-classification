# SIT definitions used in Part 3

## Contoso Change Request Reference
| Pattern | Confidence | Primary element | Supporting elements (within 300 characters) |
|---|---|---|---|
| 1 | High | Regex, word match | Keyword list: change request, product overview, specification, confidential, internal only |
| 2 | Low | Regex, word match | None |

Regex (inside the portal's word-match template):

```
(?:^|[\s,;\:\(\)\[\]"'])(CR-\d{3})(?:$|[\s,;\:\(\)\[\]"']|\.\s|\.$)
```

Recommended confidence: High.

## Contoso Project Codenames
| Pattern | Confidence | Primary element |
|---|---|---|
| 1 | Medium | Keyword list (case insensitive): Project Tailspin, Tailspin, Project 9 |

Test with `CR-test-sample.txt`: CR-227, CR-228 and CR-231 should match; CR-12 and CR-1234 should not.
