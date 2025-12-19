use iced::Task;

use super::{Message, Contact};

///
/// Actions of `Contacts` page
pub enum Action {
    None,
    Run(Task<Message>),
    Chat(Contact),
}
