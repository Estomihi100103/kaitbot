import { useState } from 'react'
import {
    Dialog,
    DialogBackdrop,
    DialogPanel,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    TransitionChild,
} from '@headlessui/react'
import {
    Bars3Icon,
    BellIcon,
    Cog6ToothIcon,
    FolderIcon,
    HomeIcon,
    XMarkIcon,
    ChatBubbleLeftIcon,
    ChatBubbleLeftRightIcon
} from '@heroicons/react/24/outline'
import { ChevronDownIcon, MagnifyingGlassIcon } from '@heroicons/react/20/solid'
import { useLocation, Link, useNavigate  } from 'react-router-dom'
import useAuth from "../../hooks/useAuth";



const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
    { name: 'Conversation', href: '/conversations', icon: ChatBubbleLeftIcon },
]

const userNavigation = [
    { name: 'Profil Anda', href: '/' },
    { name: 'Keluar', href: '/logout' },
]

function classNames(...classes) {
    return classes.filter(Boolean).join(' ')
}

export default function Layout({ children, title }) {
    const [sidebarOpen, setSidebarOpen] = useState(false)
    const location = useLocation()
    const {user, logout } = useAuth()
    const navigate = useNavigate()

    const handleLogout = () => {
        logout(); 
        navigate('/');
    };

    const SidebarContent = () => (
        <div className="flex grow flex-col gap-y-5 overflow-y-auto bg-white px-6 pb-4">
            <div className="flex h-16 shrink-0 items-center">
                <img
                    alt="KaitBot"
                    src="/logo.png"
                    className="h-12 w-auto"
                />
            </div>
            <nav className="flex flex-1 flex-col">
                <ul role="list" className="flex flex-1 flex-col gap-y-7">
                    <li>
                        <ul role="list" className="-mx-2 space-y-1">
                            {navigation.map((item) => {
                                const isCurrent = location.pathname === item.href
                                return (
                                    <li key={item.name}>
                                        <Link
                                            to={item.href}
                                            className={classNames(
                                                isCurrent
                                                    ? 'bg-gray-50 text-indigo-600'
                                                    : 'text-gray-700 hover:bg-gray-50 hover:text-indigo-600',
                                                'group flex gap-x-3 rounded-md p-2 text-sm/6 font-semibold',
                                            )}
                                        >
                                            <item.icon
                                                aria-hidden="true"
                                                className={classNames(
                                                    isCurrent ? 'text-indigo-600' : 'text-gray-400 group-hover:text-indigo-600',
                                                    'size-6 shrink-0',
                                                )}
                                            />
                                            {item.name}
                                        </Link>
                                    </li>
                                )
                            })}
                        </ul>
                    </li>
                    <li className="mt-auto">
                        <a
                            href="#"
                            className="group -mx-2 flex gap-x-3 rounded-md p-2 text-sm/6 font-semibold text-gray-700 hover:bg-gray-50 hover:text-indigo-600"
                        >
                            <Cog6ToothIcon
                                aria-hidden="true"
                                className="size-6 shrink-0 text-gray-400 group-hover:text-indigo-600"
                            />
                            Pengaturan
                        </a>
                    </li>
                </ul>
            </nav>
        </div>
    )

    return (
        <div className="h-full bg-white">
            {/* Mobile sidebar */}
            <Dialog open={sidebarOpen} onClose={setSidebarOpen} className="relative z-50 lg:hidden">
                <DialogBackdrop
                    transition
                    className="fixed inset-0 bg-gray-900/80 transition-opacity duration-300 ease-linear data-closed:opacity-0"
                />

                <div className="fixed inset-0 flex">
                    <DialogPanel
                        transition
                        className="relative mr-16 flex w-full max-w-xs flex-1 transform transition duration-300 ease-in-out data-closed:-translate-x-full"
                    >
                        <TransitionChild>
                            <div className="absolute top-0 left-full flex w-16 justify-center pt-5 duration-300 ease-in-out data-closed:opacity-0">
                                <button type="button" onClick={() => setSidebarOpen(false)} className="-m-2.5 p-2.5 cursor-pointer">
                                    <span className="sr-only">Close sidebar</span>
                                    <XMarkIcon aria-hidden="true" className="size-6 text-white" />
                                </button>
                            </div>
                        </TransitionChild>
                        <SidebarContent />
                    </DialogPanel>
                </div>
            </Dialog>

            {/* Desktop sidebar */}
            <div className="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-72 lg:flex-col">
                <div className="flex grow flex-col gap-y-5 overflow-y-auto border-r border-gray-200 bg-white px-6 pb-4">
                    <SidebarContent />
                </div>
            </div>

            <div className="lg:pl-72">
                {/* Header */}
                <div className="sticky top-0 z-40 lg:mx-auto lg:max-w-7xl lg:px-8">
                    <div className="flex h-16 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-xs sm:gap-x-6 sm:px-6 lg:px-0 lg:shadow-none">
                        <button
                            type="button"
                            onClick={() => setSidebarOpen(true)}
                            className="-m-2.5 p-2.5 text-gray-700 lg:hidden cursor-pointer"
                        >
                            <span className="sr-only">Open sidebar</span>
                            <Bars3Icon aria-hidden="true" className="size-6" />
                        </button>

                        <div aria-hidden="true" className="h-6 w-px bg-gray-200 lg:hidden" />

                        <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
                            <form action="#" method="GET" className="grid flex-1 grid-cols-1">
                                <input
                                    name="search"
                                    type="search"
                                    placeholder="Cari..."
                                    aria-label="Search"
                                    className="col-start-1 row-start-1 block size-full bg-white pl-8 text-base text-gray-900 outline-hidden placeholder:text-gray-400 sm:text-sm/6"
                                />
                                <MagnifyingGlassIcon
                                    aria-hidden="true"
                                    className="pointer-events-none col-start-1 row-start-1 size-5 self-center text-gray-400"
                                />
                            </form>
                            <div className="flex items-center gap-x-4 lg:gap-x-6">
                                <button type="button" className="-m-2.5 p-2.5 text-gray-400 hover:text-gray-500 cursor-pointer">
                                    <span className="sr-only">View notifications</span>
                                    <BellIcon aria-hidden="true" className="size-6" />
                                </button>

                                <div aria-hidden="true" className="hidden lg:block lg:h-6 lg:w-px lg:bg-gray-200" />

                                {/* Profile dropdown */}
                                <Menu as="div" className="relative">
                                    <MenuButton className="relative flex items-center cursor-pointer">
                                        <span className="absolute -inset-1.5" />
                                        <span className="sr-only">Open user menu</span>
                                        <img
                                            alt=""
                                            src="/src/assets/img/user.png"
                                            className="size-8 rounded-full bg-gray-50"
                                        />
                                        <span className="hidden lg:flex lg:items-center">
                                            <span aria-hidden="true" className="ml-4 text-sm/6 font-semibold text-gray-900">
                                                {user?.name || 'User'}
                                            </span>
                                            <ChevronDownIcon aria-hidden="true" className="ml-2 size-5 text-gray-400" />
                                        </span>
                                    </MenuButton>
                                    <MenuItems
                                        transition
                                        className="absolute right-0 z-10 mt-2.5 w-32 origin-top-right rounded-md bg-white py-2 shadow-lg ring-1 ring-gray-900/5 transition focus:outline-hidden data-closed:scale-95 data-closed:transform data-closed:opacity-0 data-enter:duration-100 data-enter:ease-out data-leave:duration-75 data-leave:ease-in"
                                    >
                                        {userNavigation.map((item) => (
                                             <MenuItem key={item.name}>
                                                {item.name === 'Keluar' ? (
                                                    <button
                                                        onClick={handleLogout}
                                                        className="block w-full text-left px-3 py-1 text-sm/6 text-gray-900 data-focus:bg-gray-50 cursor-pointer"
                                                    >
                                                        {item.name}
                                                    </button>
                                                ) : (
                                                    <Link
                                                        to={item.href}
                                                        className="block px-3 py-1 text-sm/6 text-gray-900 data-focus:bg-gray-50"
                                                    >
                                                        {item.name}
                                                    </Link>
                                                )}
                                            </MenuItem>
                                        ))}
                                    </MenuItems>
                                </Menu>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Main Content */}
                <main className="py-10">
                    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                        {title && (
                            <div className="md:flex md:items-center md:justify-between mb-8">
                                <div className="min-w-0 flex-1">
                                    <h2 className="text-2xl/7 font-bold text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight">
                                        {title}
                                    </h2>
                                </div>
                            </div>
                        )}
                        {children}
                    </div>
                </main>
            </div>
        </div>
    )
}