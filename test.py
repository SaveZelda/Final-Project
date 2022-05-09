import adbookfromkevin as AB_Final
import pytest
from adbookfromkevin import Contact
from adbookfromkevin import *
import sys

create_df()
create_favorites()
create_contacts()

def test_full_name():
    obj_1 = Contact("Kevin","Guo","9178086521","@gmail.com",'NY')
    assert obj_1.full_name() == 'Kevin Guo'

def test_edit_phone():
    obj_1 = Contact("Kevin","Guo","9178086521","@gmail.com",'NY')
    obj_1.edit_phone("2128856563")
    assert obj_1.phone == "2128856563"
    
def test_edit_location():
    obj_1 = Contact("Kevin","Guo","9178086521","@gmail.com",'NY')
    obj_1.edit_location("PA")
    assert obj_1.location == "PA"
    
def test_edit_email():
    obj_1 = Contact("Kevin","Guo","9178086521","@gmail.com",'NY')
    obj_1.edit_email("@outlook.com")
    assert obj_1.email == "@outlook.com"
    
def test_enter_wrong_number_format(capsys):
    with pytest.raises(StopIteration):
        inputs = iter(['k', 'g','hiiikkkkll'])
        AB_Final.input = lambda x: next(inputs)
        output = AB_Final.enter_contact()
    captured = capsys.readouterr()
    assert 'Please only enter numbers for phone, alphabet or others are not accepted:' in captured.out

def test_enter_wrong_number_length(capsys):
    with pytest.raises(StopIteration):
        inputs = iter(['k', 'g','10'])
        AB_Final.input = lambda x: next(inputs)
        output = AB_Final.enter_contact()
    captured = capsys.readouterr()
    assert 'Incorrect length. Please enter 10 digit:' in captured.out
        
def test_enter_wrong_email_format(capsys):
    with pytest.raises(StopIteration):
        inputs = iter(['k', 'g','9178086521','gmail.com'])
        AB_Final.input = lambda x: next(inputs)
        output = AB_Final.enter_contact()
    captured = capsys.readouterr()
    assert 'Email format incorrect. Please make sure @ and .com is included:' in captured.out

def test_enter_another_wrong_email_format(capsys):
    with pytest.raises(StopIteration):
        inputs = iter(['k', 'g','9178086521','@gmail'])
        AB_Final.input = lambda x: next(inputs)
        output = AB_Final.enter_contact()
    captured = capsys.readouterr()
    assert 'Email format incorrect. Please make sure @ and .com is included:' in captured.out
        
def test_enter_wrong_location_length(capsys):
    with pytest.raises(StopIteration):
        inputs = iter(['k', 'g','9178086521','@gmail.com','NYC'])
        AB_Final.input = lambda x: next(inputs)
        output = AB_Final.enter_contact()
    captured = capsys.readouterr()
    assert 'Format Incorrect. Please make it is only two alphabets:' in captured.out
        
def test_enter_wrong_location_format(capsys):
    with pytest.raises(StopIteration):
        inputs = iter(['k', 'g','9178086521','@gmail.com','222'])
        AB_Final.input = lambda x: next(inputs)
        output = AB_Final.enter_contact()
    captured = capsys.readouterr()
    assert 'Format Incorrect. Only alphabets accepted:' in captured.out

# Because we have not created any contact, the contact and favorite list should be empty

def test_empty_contact(capsys):
    output = AB_Final.display_contact()
    captured = capsys.readouterr()
    assert 'There is no existing contact in the address book' in captured.out

def test_empty_favorites(capsys):
    output = AB_Final.display_favorite()
    captured = capsys.readouterr()
    assert 'There is no existing favorite contact in the address book' in captured.out

# Now we enter some contacts for testing
def test_enter_contact(capsys):
    inputs = iter(['k', 'g','9178086521','@gmail.com','NY'])
    AB_Final.input = lambda x: next(inputs)
    output = AB_Final.enter_contact()
    return_df()
    captured = capsys.readouterr()
    assert 'Contacts Created' in captured.out
    assert df.iloc[0].to_list() == ['k', 'g', 9178086521, '@gmail.com', 'NY']
    
def test_enter_new_contact(capsys):
    inputs = iter(['j', 'z','9298086521','@gmail.com','NY'])
    AB_Final.input = lambda x: next(inputs)
    output = AB_Final.enter_contact()
    return_df()
    captured = capsys.readouterr()
    assert 'Contacts Created' in captured.out
    assert df.iloc[1].to_list() == ['j', 'z', 9298086521,'@gmail.com','NY']
    
def test_add_favorites():
    inputs = iter(['k',0])
    AB_Final.input = lambda x: next(inputs)
    output = AB_Final.add_favorite()
    return_favorites()
    assert favorites[0] == Contact('k', 'g', 9178086521, '@gmail.com', 'NY')

# Because there is currently only one user has first name k, user should only be able to 
# choose index 0 instead of other index to accidentally add other contact
def test_cannot_add_favorites_wrong_entry(capsys):
    inputs = iter(['k',1])
    AB_Final.input = lambda x: next(inputs)
    output = AB_Final.add_favorite()
    captured = capsys.readouterr()
    assert 'Invalid Entry. Please try again.' in captured.out

# Because we add 2 contacts, now lets see how many contacts we have
def test_only_two_contact():
    return_df()
    assert len(df) == 2
    
# Because we add 1 favorite, now lets see how many favorite we have
def test_only_one_favorite():
    return_favorites()
    assert len(favorites) == 1
    
def test_enter_third_contact():
    inputs = iter(['e', 'c','2128086521','@outlook.com','PA'])
    AB_Final.input = lambda x: next(inputs)
    output = AB_Final.enter_contact()
    return_df()
    assert df.iloc[2].to_list() == ['e', 'c',2128086521,'@outlook.com','PA']
    
def test_email_filter_contact():
    inputs = iter([1,'gmail'])
    AB_Final.input = lambda x: next(inputs)
    output = AB_Final.filter_contact()
    assert output['Email'].unique() == '@gmail.com' and len(output) == 2
    
def test_location_filter_contact():
    inputs = iter([2,'ny'])
    AB_Final.input = lambda x: next(inputs)
    output = AB_Final.filter_contact()
    assert output['Location'].unique() == 'NY' and len(output) == 2

# Used to be NY, now lets change it into NJ
def test_edit_location_once():
    inputs = iter(['k','0','5','NJ','n'])
    AB_Final.input = lambda x: next(inputs)
    output = AB_Final.edit_info()
    return_df()
    assert df.iloc[0].to_list() == ['k', 'g', 9178086521, '@gmail.com', 'NJ']

# Instead of jumping out of the loop, let's stay in the loop and edit two elements in one control
def test_edit_email_and_number():
    inputs = iter(['k','0','4','@outlook.com','y','3','9299990000','n'])
    AB_Final.input = lambda x: next(inputs)
    output = AB_Final.edit_info()
    return_df()
    assert df.iloc[0].to_list() == ['k', 'g', 9299990000, '@outlook.com', 'NJ']

def test_delete_contact():
    inputs = iter(['k',0])
    AB_Final.input = lambda x: next(inputs)
    output = AB_Final.delete_contact()
    temp_contact = return_contacts()
    temp = []
    for i in range (len(temp_contact)):
        temp.append(temp_contact[i].first_name)
    assert 'k' not in temp and len(temp_contact) == 2
    
def test_invalid_number_option_entry(capsys):
    with pytest.raises(StopIteration):
        inputs = iter([10])
        AB_Final.input = lambda x: next(inputs)
        output = AB_Final.Address_Book()
    captured = capsys.readouterr()
    assert 'Invalid option. Please try again: ' in captured.out

def test_invalid_character_option_entry(capsys):
    with pytest.raises(StopIteration):
        inputs = iter(['hi'])
        AB_Final.input = lambda x: next(inputs)
        output = AB_Final.Address_Book()
    captured = capsys.readouterr()
    assert 'Characters selection not supported. Please try again: ' in captured.out

# Pep is not in the address book, lets see how it plays out
def test_no_such_person_in_edit(capsys):
    inputs = iter(['pep'])
    AB_Final.input = lambda x: next(inputs)
    output = AB_Final.edit_info()
    assert output == None
    captured = capsys.readouterr()
    assert 'There is no such person. Please try again' in captured.out

def test_no_such_person_in_lookup(capsys):
    inputs = iter(['pep'])
    AB_Final.input = lambda x: next(inputs)
    output = AB_Final.lookup_contact()
    assert output == None
    captured = capsys.readouterr()
    assert 'No person found. Please try again' in captured.out

# Let's test export function and program termination
def test_export_csv(capsys):
    output = AB_Final.export_csv()
    captured = capsys.readouterr()
    assert 'Successfully exported all contacts!' in captured.out
    
def test_terminate_program(capsys):
    inputs = iter([0])
    AB_Final.input = lambda x: next(inputs)
    output = AB_Final.Address_Book()
    captured = capsys.readouterr()
    assert output == None
    assert 'Thank you. Goodbye!'

    
