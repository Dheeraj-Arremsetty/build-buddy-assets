Of course. Here is a comprehensive demo presentation script for the "Barista Onboarding Agent" use case, designed for a 15-20 minute presentation.

---

## IBM watsonx Orchestrate Demo Script: The Barista Buddy

**Presenter:** [Your Name/Title]
**Audience:** HR and Operations Leadership at a rapidly growing coffee company
**Total Time:** 20 Minutes

---

### **Section 1: Introduction & The Business Challenge (3 Minutes)**

**[Presenter Talking Points]**

"Good morning, everyone. Thank you for your time today. We've been following your company's impressive growth, and it's clear you're building something special. Your brand is synonymous with quality coffee and a great customer experience.

But we also understand that rapid growth presents unique operational challenges. As you open new stores and hire dozens of new baristas each month, your most valuable assets—your experienced store managers—are getting pulled away from the floor.

They're spending hours each week answering the same set of questions from new hires:
*   'What's the dress code?'
*   'How do I set up direct deposit?'
*   'When is my first training session on the espresso machine?'
*   'Where can I find the benefits guide?'

This constant interruption not only impacts the manager's ability to coach their team and engage with customers, but it also creates an inconsistent onboarding experience for your new employees. Some get quick answers, others have to wait. This friction can slow down their time-to-productivity and even affect morale.

The core challenge is this: **How do you scale your onboarding process to support rapid growth, while empowering your new hires and giving your managers their time back?**"

**[Key Message]**
Your current onboarding process is a manual bottleneck that doesn't scale. It's costing your managers valuable time and creating an inconsistent experience for new employees.

---

### **Section 2: The Solution: The "Barista Buddy" powered by watsonx Orchestrate (3 Minutes)**

**[Presenter Talking Points]**

"That's the exact problem we're here to solve with IBM watsonx Orchestrate. We're not talking about a simple, generic chatbot. We're talking about building a dedicated, AI-powered digital teammate for your company—an agent we're calling the **'Barista Buddy.'**

Imagine giving every new hire, on their very first day, an expert resource they can ask anything. The Barista Buddy is designed to do two key things:

1.  **Provide Instant, Accurate Answers:** It has access to your specific company documents—the employee handbook, benefits guides, and training schedules. It uses this knowledge to provide instant, consistent answers to policy and procedure questions.
2.  **Take Action:** It goes beyond just answering questions. It can initiate HR and IT workflows, like sending out forms or creating support tickets, directly from the conversation.

This is made possible by a powerful, multi-agent architecture built with the watsonx Orchestrate Agent Builder.

*(Optional: Display a simple architecture slide)*

At the front is the **Barista Buddy Supervisor Agent**. It's the main point of contact that understands the user's request. Behind the scenes, it intelligently routes tasks to specialized **Collaborator Agents**:
*   An **Onboarding Knowledge Agent** that specializes in finding answers from your documents.
*   An **HR Actions Agent** that specializes in performing tasks like sending emails or creating tickets.

The result is a highly capable, scalable, and secure system that works 24/7. It frees your managers to focus on what they do best—running a great coffee shop—and empowers your new baristas to get up to speed faster than ever before."

**[Business Value Proposition]**
The Barista Buddy transforms onboarding from a manual, manager-dependent process into an automated, self-service experience. This accelerates new hire productivity, improves manager effectiveness, and ensures operational consistency across all your locations.

---

### **Section 3: Live Demonstration: A Day in the Life of a New Barista (8 Minutes)**

**[Presenter Talking Points]**

"Now, let's see the Barista Buddy in action. I'm going to play the role of a new hire on their first day, and I'll interact with the agent just like they would.

**[Action: Open the watsonx Orchestrate chat interface showing the Barista Buddy agent.]**

#### **Scenario 1: Foundational Knowledge Question (RAG)**

"Okay, first things first. I need to know what to wear. Let me ask the Barista Buddy."

**[Action: Type the following prompt into the chat:]**
> "What is the dress code for baristas?"

**[Expected Outcome]**
The agent will process the request and respond with a clear, concise answer sourced directly from the `barista_employee_handbook.pdf`. The response should detail the required attire (e.g., company-issued apron, black or khaki pants, non-slip shoes).

**[Presenter Talking Points]**
"And there it is. A perfect, accurate answer in seconds. Notice it didn't just give a vague reply; it provided the specific details from the handbook. The `Onboarding_Knowledge_Agent` used Retrieval-Augmented Generation, or RAG, to find the exact passage in your document and generate a natural language answer. My manager didn't have to stop what they were doing, and I have the correct information immediately."

---

#### **Scenario 2: Action-Oriented Request (Tool Use)**

"Great. Now that I know what to wear, I need to get paid. I'll ask the agent how to set up my direct deposit."

**[Action: Type the following prompt into the chat:]**
> "I need to set up my direct deposit."

**[Expected Outcome]**
The agent will understand the intent is to perform an action. It will invoke the `send_form_by_email` tool from the `HR_Actions_Agent`. The chat will display a confirmation message similar to: `{"status": "success", "message": "The 'Direct Deposit' form has been successfully sent to [your_email@example.com]."}`.

**[Presenter Talking Points]**
"This is where watsonx Orchestrate goes beyond a simple Q&A bot. The Barista Buddy didn't just tell me *how* to set up direct deposit; it *initiated the process*. The Supervisor Agent recognized this was a task, not a question, and passed it to the `HR_Actions_Agent`. That agent then used a custom tool we built to send the correct form to my email. We've just automated a key HR workflow, saving time for both me and the HR team."

---

#### **Scenario 3: Complex Request & Intelligent Escalation (Multi-Agent Routing)**

"Okay, for my last task, I have a more complex issue. I can't find my training schedule, and I think my new company laptop might have an issue."

**[Action: Type the following prompt into the chat:]**
> "I can't access my new hire training schedule and my laptop login isn't working. Can you help?"

**[Expected Outcome]**
This will trigger the multi-agent logic.
1.  The **Barista Buddy (Supervisor)** will first try to solve the training schedule part by routing to the **Onboarding Knowledge Agent**. The agent might respond with information from the `new_hire_training_schedule.csv`.
2.  Recognizing it cannot fix a broken laptop, the Supervisor will then route the second part of the request to the **HR Actions Agent**.
3.  This agent will invoke the `create_support_ticket` tool. The chat will display a confirmation like: `{"status": "success", "message": "A support ticket has been created. A team member will reach out shortly.", "ticket_id": "TICKET-ABC12345"}`.

**[Presenter Talking Points]**
"This is the most powerful part of the demo. The Barista Buddy understood my request had two distinct parts. It first tried to answer my question about the training schedule using its knowledge base.

But it also recognized that a broken laptop is something it can't fix itself. Instead of just saying 'I can't help,' the Supervisor Agent intelligently routed the problem to the `HR_Actions_Agent`, which automatically created an IT support ticket. I now have a ticket number, and the right team has been notified. This is true orchestration—seamlessly combining knowledge retrieval, task automation, and intelligent escalation."

---

### **Section 4: A Quick Look Under the Hood (2 Minutes)**

**[Presenter Talking Points]**

"What you just saw looks complex, but building it with the watsonx Orchestrate Agent Development Kit, or ADK, is remarkably straightforward. This isn't a massive coding project.

*   **[Action: Briefly show the `barista_buddy_agent.yaml` file]**
    "We define our agents in simple, readable YAML files. Here, you can see we've given our Supervisor agent clear instructions and told it which collaborator agents and tools it can use."

*   **[Action: Briefly show the `hr_actions.py` file]**
    "The tools that perform actions are just Python functions. This `send_form_by_email` function is simple, well-documented, and easily connected to your real systems, whether it's an email API or a direct integration with Workday or ServiceNow."

*   **[Action: Briefly show the `onboarding_kb.yaml` file]**
    "And connecting your knowledge is as simple as pointing to the documents. Orchestrate handles the complex process of embedding and indexing them in a vector database for you."

**[Technical Highlight]**
The power of the ADK lies in its declarative, low-code approach. You define *what* you want the agent to do, and Orchestrate handles the *how*. This makes building and maintaining sophisticated AI agents accessible to your existing development teams.

---

### **Section 5: Q&A and Common Questions (2 Minutes)**

**[Presenter Talking Points]**

"I'll pause there to answer any questions you might have. Some common questions we get are:"

*   **Q: How secure is this? Can a new hire access sensitive information?**
    *   **A:** Security is paramount. Access is controlled at multiple levels. The knowledge base only contains information appropriate for new hires. The tools themselves have permissions; for example, a tool to approve vacation could be restricted to manager-level agents.

*   **Q: Can this connect to our existing HR systems, not just simulate actions?**
    *   **A:** Absolutely. The Python tools are fully customizable. We can build them to make secure API calls to virtually any modern system, including Workday, SAP, or your internal IT service desk.

*   **Q: How do we update the knowledge? Is it complicated?**
    *   **A:** It's incredibly simple. When you update your employee handbook, you just replace the file and have Orchestrate re-process it. There's no need to manually retrain a model.

---

### **Section 6: Next Steps & Call to Action (2 Minutes)**

**[Presenter Talking Points]**

"What you've seen today is just the beginning. The Barista Buddy solves a critical onboarding challenge, delivering significant business value:

*   **Increased Manager Productivity:** By saving each store manager just 2-3 hours per week, you're giving hundreds of hours back to coaching and customer-facing activities.
*   **Accelerated Employee Ramp-Up:** New hires get answers instantly, helping them become confident, productive members of the team faster.
*   **Improved Consistency and Compliance:** Every employee gets the same, accurate information, reducing errors and ensuring everyone follows the correct procedures.

This is a strategic investment in your operational backbone that directly supports your growth.

Our recommended next step is a **half-day discovery workshop**. In this session, our experts will sit down with your HR and Operations teams to map out your top 3-5 onboarding workflows. From there, we can build a production-ready pilot of the Barista Buddy in a matter of weeks, not months.

Thank you for your time. I look forward to discussing how we can partner to build your future workforce experience."