use iced::Length::Fill;
use iced::widget::{button, container, text};
use iced::{Element, Task, Theme};

use crate::contacts::Contacts;
use crate::conversation::Conversation;
use crate::github::Report;

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
        Message::Contacts(message) => {
            if let Screen::Contacts(contacts) = &mut state.screen {
                let action = contacts.update(message);

                match action {
                    contacts::Action::None => Task::none(),
                    contacts::Action::Run(task) => task.map(Message::Contacts),
                    contacts::Action::Chat(contact) => {
                        let (conversation, task) = Conversation::new(contact);

                        state.screen = Screen::Conversation(conversation);

                        task.map(Message::Conversation)
                    }
                 }
            } else {
                Task::none()    
            }
        }
        Message::Conversation(message) => {
            if let Screen::Conversation(conversation) = &mut state.screen {
                conversation.update(message).map(Message::Conversation)
            } else {
                Task::none()    
            }
        }
    }
    // match message {
    //     Message::Increment => state.count += 1,
    //     Message::FetchWeather => Task::perform(
    //         fetch_weather(),
    //         Message::WeatherFetched,
    //     ),
    //     Message::WeatherFetched(weather) => {
    //         state.weather = Some(weather);
    //         Task::none()
    //    }
    // }
}

fn view(state: &State) -> Element<'_, Message> {
    container(
        column![
            "Top",
            row!["Left", "Right"].spacing(10),
            "Bottom"
        ]
        .spacing(10)
    )
    .padding(10)
    .center_x(Fill)
    .center_y(Fill)
    .into()
}

fn theme(state: &State) -> Theme {
    Theme::TokyoNight
}
pub mod github {
    #[derive(Debug, Clone)]
    pub enum Message {
        FetchWeather,
        WeatherFetched(Weather),
    }
    #[derive(Debug, Clone)]
    pub struct Weather {}
    pub struct Report {}
}
pub mod contacts {
    #[derive(Debug, Clone)]
    pub struct Contacts {}
    #[derive(Debug, Clone)]
    pub struct Message {}
}
pub mod conversation {
    #[derive(Debug, Clone)]
    pub struct Conversation {}
    #[derive(Debug, Clone)]
    pub struct Message {}
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
    Contacts(contacts::Message),
    Conversation(conversation::Message)
}
