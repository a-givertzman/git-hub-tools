mod infrostruct;
mod presentation;
use iced::{Element, Task, Theme};

use crate::presentation::{
    Contacts, contacts,
    Conversation, conversation,
    Report, report,
};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    iced::application(new, update, view)
        .theme(theme)
        .run()?;
    println!("Hello, world!");
    Ok(())
}

fn new() -> State {
    Default::default()
}

fn update(state: &mut State, message: Message) -> Task<Message> {
    match message {
        Message::Increment => {
            state.count += 1;
            Task::none()
        }
        Message::Report(message) => {
            match message {
                report::Message::FetchReport => Task::perform(
                    fetch_weather(),
                    report::Message::ReportFetched,
                ),
                report::Message::ReportFetched(weather) => {
                    state.page = Some(weather);
                    Task::none()
               }
            }
            if let Page::Report(report) = &mut state.page {
                report.update(message).map(Message::Report)
            } else {
                Task::none()    
            }
        }
        Message::Contacts(message) => {
            if let Page::Contacts(contacts) = &mut state.page {
                let action = contacts.update(message);
                match action {
                    contacts::Action::None => Task::none(),
                    contacts::Action::Run(task) => task.map(Message::Contacts),
                    contacts::Action::Chat(contact) => {
                        let (conversation, task) = Conversation::new(contact);

                        state.page = Page::Conversation(conversation);

                        task.map(Message::Conversation)
                    }
                 }
            } else {
                Task::none()    
            }
        }
        Message::Conversation(message) => {
            if let Page::Conversation(conversation) = &mut state.page {
                conversation.update(message).map(Message::Conversation)
            } else {
                Task::none()    
            }
        }
    }
}

fn view(state: &State) -> Element<'_, Message> {
    match &state.page {
        Page::Report(report) => report.view().map(Message::Report),
        Page::Contacts(contacts) => contacts.view().map(Message::Contacts),
        Page::Conversation(conversation) => conversation.view().map(Message::Conversation),
    }
}

fn theme(state: &State) -> Theme {
    Theme::TokyoNight
}
struct State {
    count: u64,
    page: Page
}
enum Page {
    Report(Report),
    Contacts(Contacts),
    Conversation(Conversation),
}

impl Default for State {
    fn default() -> Self {
        Self {
            count: Default::default(),
            page: Page::Contacts(Contacts {  }),
        }
    }
}

#[derive(Debug, Clone)]
enum Message {
    Increment,
    Report(report::Message),
    Contacts(contacts::Message),
    Conversation(conversation::Message)
}
