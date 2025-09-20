#!/usr/bin/env python3
"""
Process the transcript content to remove timestamps and structure it properly.
"""

# Read the raw content from the file
content = """0:00
Picture this. You flop top pair in a four-way pot and suddenly you're stuck. Do you check, bet, take your pants off,
0:06
and roll around on the floor? As one of our viewers astutely commented on a recent video, "Multi-way pots are 95% of
0:12
what we face, but most poker content only focuses on heads up." I think he's right. So, today we're going to fix
0:18
that. We're going to focus on multi-way. And in this video, you're going to learn when to bet or when to check as the pre
0:23
flop razor. You'll learn how to size correctly when you are multi-way. You'll learn when to bluff, when to don bet,
0:29
and maybe most importantly, the five biggest red flags that most players miss when they are playing multi-way pots.
0:35
This is the same system we teach our top students, some of whom are now earning over $100 an hour. But I want to make
0:40
clear, we don't make any income or win rate guarantees. These results are atypical, and you most likely won't achieve them because I can't sit behind
0:47
you and whisper in your ear what to do each hand. What we can do, though, is pass down the exact lessons that our
0:52
best students are using right now to crush multi-way pots. If you've ever been stuck in a bloated multi-way pot
0:58
with no plan, this is the video that gives you one. Let's jump in. All right, you guys know I'm a big fan of flowcharts. So, let's start with a
Flowchart
1:04
flowchart. And when we are multi-way as the pre flop razor, the first question I like to ask is, is this flop likely to
1:11
get stabbed? When we look at what makes this a yes, what makes it more likely if the board is wet? Right? If there is a
1:16
flush draw out there, if there are a bunch of straight draws out there, it is going to be more likely to get stabbed. Also, more likely to get stabbed if the
1:23
board is dynamic. This is kind of a cousin of wet, but this just means are the nuts likely to change on the turn.
1:28
So, a dynamic board could be dry like 74 deuce rainbow, but if you look at this board, pretty much every card in the
1:35
deck except a seven is going to change the nut. But in general, the more wet and the more dynamic the board, more
1:41
likely it is to get stabbed. The final factor that makes it more likely to get stabbed is the amount of players left to act behind us as the pre flop razor. So,"""

# Process the content
lines = content.split('\n')
cleaned_lines = []

for line in lines:
    line = line.strip()
    
    # Skip empty lines
    if not line:
        continue
        
    # Skip timestamps
    if line and line[0].isdigit() and ':' in line and len(line) <= 5:
        continue
        
    # Check for section headers
    if line in ['Flowchart', 'Examples', 'Hand Strength', 'bluffs', 'preflop razer', 'preflop caller', 'when to call', 'when to pounce', 'when to donk', 'next to act', 'check back', 'flop dontk', 'check raise']:
        cleaned_lines.append(f"\n## {line}\n")
        continue
        
    # Regular content
    if line:
        cleaned_lines.append(line)

# Join and clean up
cleaned_content = ' '.join(cleaned_lines)
cleaned_content = cleaned_content.replace('  ', ' ')

print("First part processed:")
print(cleaned_content[:500])
print("...")
